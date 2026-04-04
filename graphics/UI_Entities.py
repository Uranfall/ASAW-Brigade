import math
import time

import pygame.draw

from Entity import Entity
from graphics.graphics_utility import Camera


class UIEntity(Entity):
    LIFETIME = 5

    def __init__(self, position: tuple[int, int], rotation: float, time_offset=0.0):
        super().__init__(position, rotation)
        self.creation_time = time.time()+time_offset

    def get_age(self):
        return time.time()-self.creation_time

    def get_progress(self):
        return self.get_age()/self.__class__.LIFETIME


class ExpandingCircle(UIEntity):
    COLOR = (50, 50, 255)
    LIFETIME = 0.25
    FINAL_SIZE = 20

    def __init__(self, position: tuple[int, int], time_offset=0.0):
        super().__init__(position, 0, time_offset)

    def draw(self, camera: Camera):
        pygame.draw.circle(camera.screen,
                           self.__class__.COLOR,
                           camera(*self.position),
                           math.ceil(camera(self.__class__.FINAL_SIZE*self.get_progress())),
                           math.ceil(camera(2)))
