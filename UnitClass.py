from __future__ import annotations
import math
import pygame
from shared_utility import *
from Entity import Entity
from graphics.graphics_utility import Camera


class Unit(Entity):

    def __init__(self,
                 # unit_type: str,
                 position: tuple[int, int],
                 rotation: float,
                 speed: int,
                 #team: int,

                 selected: bool,
                 act_list = list["idle"]):
        super().__init__(position, rotation, selected)
        self.target_pos = position
        self.target_rotation = rotation
        self.team = 0
        self.target = None
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

    def calc_rotation(self):
        #for self: when we add unit targeting, check if enemy is in range
        targetX = self.target_pos[0]-self.position[0]
        targetY = self.target_pos[1]-self.position[1]
        self.rotation = vector_to_angle((targetX, targetY))


    def calc_movement(self):
        # y distance and x distance divided by fps
        #for self: get this shit running at the same velocity

        currentX = self.position[0]
        currentY = self.position[1]
        targetX = self.target_pos[0]
        targetY = self.target_pos[1]
        if not is_within_box((currentX, currentY), get_collision_points((targetX, targetY), (5,5))):
            dx, dy = (targetX - currentX, targetY - currentY)
            stepx, stepy = (dx / 60., dy / 60.)
            self.position = (currentX+self.change_rate[0], currentY+self.change_rate[1])
            self.change_rate = [stepx, stepy]
        else:
            self.change_rate = [0,0]


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
                               int(camera(max(self.IMAGE.get_size())*self.IMAGE_SCALE)/2),
                               math.ceil(camera(5)))
        super(Unit, self).draw(camera)






