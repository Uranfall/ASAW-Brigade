from __future__ import annotations
import math
import pygame
from Entity import Entity
from graphics.graphics_utility import Camera


class Unit(Entity):

    def __init__(self,
                 # unit_type: str,
                 position: tuple[int, int],
                 rotation: float,
                 speed: int,
                 selected: bool,
                 act_list: list = ["idle"]):
        super().__init__(position, rotation, selected)
        self.target_pos = position
        self.target_rotation = rotation
        self.selected = selected
        self.speed = 1
        #self.unit_type = unit_type

    def calc_movement_and_rotation(self):
        # finding the function from unit pos to target pos, simple algebra
        change_rate = 1
        if self.target_pos[0] > self.position[0]:
            change_rate = change_rate * -1

        if self.target_pos[0] != self.position[0]:
            m = self.position[1] - self.target_pos[1] / self.position[0] - self.target_pos[0]
            b = self.position[1] - self.position[0] * m
            x = self.position[0] + change_rate * self.speed
            y = m * x + b
            self.position = (x, y)

        else:
            y = self.position[1] + change_rate * self.speed
            self.position = (self.position[0], y)



    def draw(self, camera: Camera):
        if self.selected:
            pygame.draw.circle(camera.screen,
                               (32, 155, 255),
                               camera(*self.position),
                               int(camera(self.__class__.SHAPE_SIZE_ADJUST * max(self.__class__.IMAGE.get_size()))),
                               math.ceil(camera(5)))
        super(Unit, self).draw(camera)






