import math
import random

import pygame.image

from Entity import Entity
from graphics.graphics_utility import Camera
from shared_utility import snap_to_grid


DEFAULT_TILE_DISTANCE = 800


class GroundChunk(Entity):

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

    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self.tiles = [[[random.randint(9, 11), random.randint(99, 101), random.randint(9, 11)]
                       for _ in range(2)] for _ in range(2)]

    def draw(self, camera: Camera):
        scale = [camera(DEFAULT_TILE_DISTANCE/2)]*2
        offset = (DEFAULT_TILE_DISTANCE/2.5)
        for x in range(0, 2):
            for y in range(0, 2):
                new_pos = camera(self.position[0]+x*offset, self.position[1]+y*offset)
                pygame.draw.circle(camera.screen, self.tiles[x][y], new_pos, scale[0])


class Ground(Entity):
    def __init__(self, position: tuple[int, int]=(0, 0)):
        super().__init__(position, 0)
        self.tiles: dict[tuple[int, int], GroundChunk] = dict()
        self.collision = False
        self.tile_distance = DEFAULT_TILE_DISTANCE

    def draw(self, camera: Camera):
        to_render = []
        multiply_x = max(1.0, camera.screen.get_width()/camera.screen.get_height())
        multiply_y =max(1.0, 1/multiply_x)
        for row in range(-2, int(500*multiply_x/self.tile_distance/camera.zoom)+2):
            for y in range(-2, int(500*multiply_y/self.tile_distance/camera.zoom)+2):
                x, y = camera.screen_to_global(row*self.tile_distance*camera.get_zoom(),
                                               y*self.tile_distance*camera.get_zoom())
                x, y = snap_to_grid((x, y), self.tile_distance, keep_scale=False)
                if self.tiles.get((x, y)) is None:
                    self.tiles[(x, y)] = NonImageChunk((x*self.tile_distance, y*self.tile_distance))
                to_render.append(self.tiles[(x, y)])
        to_render.sort(key=lambda t: hash(t.position))  # This makes sure the chunks are rendered in random order.
        for tile in to_render:
            tile.draw(camera)



