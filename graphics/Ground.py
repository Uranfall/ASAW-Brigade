import math
import random

import pygame.image

from Entity import Entity
from graphics.graphics_utility import Camera


class GroundChunk(Entity):

    AVAILABLE_TILES = [
        pygame.image.load('./Sprites/Tiles/Ground/ground_tile.png'),
        pygame.image.load('./Sprites/Tiles/Ground/grass_tile.png'),
        pygame.image.load('./Sprites/Tiles/Ground/grass_tile2.png'),
        pygame.image.load('./Sprites/Tiles/Ground/mud_tile.png'),
    ]

    def __init__(self, position: tuple[int, int]):
        super().__init__(position, 0)
        self.tiles = [[random.choice(self.__class__.AVAILABLE_TILES) for _ in range(2)] for _ in range(2)]

    def draw(self, camera: Camera):
        scale = [camera(300)]*2
        for x in range(0, 2):
            for y in range(0, 2):
                img = self.tiles[x][y]
                new_pos = camera(self.position[0]+250*x, self.position[1]+250*y)
                img = pygame.transform.scale(img, scale)
                camera.screen.blit(img, new_pos)


class Ground(Entity):
    def __init__(self, position: tuple[int, int]=(0, 0)):
        super().__init__(position, 0)
        self.tiles: dict[tuple[int, int], GroundChunk] = dict()

    def draw(self, camera: Camera):
        for x in range(-math.ceil((500/camera.get_zoom()) / 500),
                       math.ceil((500/camera.get_zoom()) / 500) + 1):
            for y in range(-math.ceil((500/camera.get_zoom()) / 500),
                           math.ceil((500/camera.get_zoom()) / 500) + 1):
                x, y = camera(x*500, y*500)
                x, y = x//500, y//500
                print(x, y)
                if self.tiles.get((x, y)) is None:
                    self.tiles[(x, y)] = GroundChunk(camera.screen_to_global(x*500, y*500))
                self.tiles[(x, y)].draw(camera)



