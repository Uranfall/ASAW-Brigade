import math
import random

import pygame.image

from Entity import Entity
from graphics.graphics_utility import Camera
from shared_utility import snap_to_grid, lerp

tile_distance = 800
quality = 200


class GroundChunk(Entity):

    """
    A peace of ground.
    Contains multiple images inside of it.
    """

    AVAILABLE_TILES = [
        # pygame.image.load('./Sprites/Tiles/Ground/ground_tile.png'),
        pygame.image.load('./Sprites/Tiles/Ground/grass_tile.png'),
        pygame.image.load('./Sprites/Tiles/Ground/grass_tile2.png'),
        # pygame.image.load('./Sprites/Tiles/Ground/mud_tile.png'),
    ]

    def __init__(self, position: tuple[int, int]):
        super().__init__(position, 0)
        self.tiles = [[random.choice(self.AVAILABLE_TILES) for _ in range(2)] for _ in range(2)]

    def draw(self, camera: Camera):
        scale = [camera(300)]*2
        for x in range(0, 2):
            for y in range(0, 2):
                img = self.tiles[x][y]
                new_pos = camera(self.position[0]+250*x, self.position[1]+250*y)
                img = pygame.transform.scale(img, scale)
                camera.screen.blit(img, new_pos)
                # pygame.draw.circle(camera.screen, (0, 0, 255), new_pos, scale[0]/4)


class NonImageChunk(GroundChunk):
    """
    The same piece of ground as GroundChunk but instead of images uses circles.
    """

    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self.tiles = [[[random.randint(9, 11), random.randint(99, 101), random.randint(9, 11)]
                       for _ in range(2)] for _ in range(2)]

    def draw(self, camera: Camera):
        scale = [camera(tile_distance / 2)] * 2
        offset = (tile_distance / 2.5)
        for x in range(0, 2):
            for y in range(0, 2):
                new_pos = camera(self.position[0]+x*offset, self.position[1]+y*offset)
                pygame.draw.circle(camera.screen, self.tiles[x][y], new_pos, scale[0])


class Ground(Entity):
    RENDER_LAYER = 0

    """
    Contains ground chunks.
    Renders them only when the camera can see them and then stores them in memory so they stay consistent.
    The chunks are stored on server so both clients will see a slightly different ground.
    """

    def __init__(self, position: tuple[int, int]=(0, 0)):
        super().__init__(position, 0)
        self.tiles: dict[tuple[int, int], GroundChunk] = dict()
        self.collision = False

    def draw(self, camera: Camera):
        to_render = []
        min_render_size = min(camera.screen.get_size())/quality
        render_size = camera(tile_distance / 2)
        destroy_ratio = 1/render_size*min_render_size

        multiply_x = max(1.0, camera.screen.get_width()/camera.screen.get_height())
        multiply_y =max(1.0, 1/multiply_x)
        if destroy_ratio > 1:
            return
        for row in range(-2,
                         int(500*multiply_x/tile_distance/camera.zoom)+2,
                         1+round(1*destroy_ratio)):
            for y in range(-2,
                           int(500*multiply_y/tile_distance/camera.zoom)+2,
                           1 + round(1 * destroy_ratio)):
                x, y = camera.screen_to_global(row*tile_distance*camera.get_zoom(),
                                               y*tile_distance*camera.get_zoom())
                x, y = snap_to_grid((x, y), tile_distance, keep_scale=False)
                if self.tiles.get((x, y)) is None:
                    self.tiles[(x, y)] = NonImageChunk((x*tile_distance, y*tile_distance))
                to_render.append(self.tiles[(x, y)])
        to_render.sort(key=lambda t: hash(t.position))  # This makes sure the chunks are rendered in random order.
        # for tile in to_render[int(len(to_render)/render_size*min_render_size):]:
        for tile in to_render:
            tile.draw(camera)



