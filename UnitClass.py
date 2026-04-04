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
                 act_list = list["idle"]):
        super().__init__(position, rotation, selected)
        self.target_pos = position
        self.target_rotation = rotation
        self.selected = selected
        self.speed = 1
        #self.unit_type = unit_type

    def get_position(self):
        return list(self.position)
    def get_target_pos(self):
        return list(self.target_pos)
    def set_position(self, updated_pos):
        self.position = updated_pos
    def set_target_pos(self, updated_pos):
        self.target_pos = updated_pos

    def calc_movement_and_rotation(self):
        # finding the function from unit pos to target pos, simple algebra
        change_rateX = 1
        change_rateY = 1
        currentX = self.position[0]
        currentY = self.position[1]
        targetX = self.target_pos[0]
        targetY = self.target_pos[1]


        #differnt x and y
        if targetX != currentX and targetY != currentY:
            if targetX < currentX:
                change_rateX = change_rateX * -1
            if targetY < currentY:
                change_rateY = change_rateY * -1
            x = currentX + change_rateX * self.speed
            y = currentY + change_rateY * self.speed
            self.position = (x, y)
        #different y
        elif targetX == currentX and targetY != currentY:
            if targetY < currentY:
                change_rateY = change_rateY * -1
            y = currentY + change_rateY * self.speed
            self.position = (currentX, y)
        # different x
        elif targetX != currentX and targetY == currentY:
            if targetX > currentX:
                change_rateX = change_rateX * -1
            x = currentY + change_rateX * self.speed
            self.position = (x, currentY)
        #cancel
        else:
            return


    def idle(self):
        ...
    def attack(self):
        ...
    def interact(self):
        ...
    def draw(self, camera: Camera):
        if self.selected:
            pygame.draw.circle(camera.screen,
                               (32, 155, 255),
                               camera(*self.position),
                               int(camera(self.__class__.SHAPE_SIZE_ADJUST * max(self.__class__.IMAGE.get_size()))),
                               math.ceil(camera(5)))
        super(Unit, self).draw(camera)






