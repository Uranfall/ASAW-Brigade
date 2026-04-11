from __future__ import annotations
import math
import pygame
from logic_utility import *
import GlobalVariables
import Unit_AI
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
                 act_list = list["idle"],
                 ):
        super().__init__(position, rotation, selected)
        self.current_node = None
        self.path = None
        self.target_pos = position
        self.old_position = position
        self.target_rotation = rotation
        self.change_rate = [0,0]
        self.team = 0
        self.target = None
        self.selected = selected
        self.speed = 1
        #self.unit_type = unit_type

    def set_position(self, position: tuple[int, int]):
        self.position = position
    def get_position(self):
        return list(self.position)

    def get_collision_points(self):
        scale = self.IMAGE_SCALE
        img = self.IMAGE
        dimensions = (img.get_width() * scale, img.get_height() * scale)
        return get_collision_points(self.position, dimensions)


    def calc_rotation(self):
        #for self: when we add unit targeting, check if enemy is in range
        targetX = self.target_pos[0]-self.position[0]
        targetY = self.target_pos[1]-self.position[1]
        self.rotation = vector_to_angle((targetX, targetY))


    def calc_movement(self, grid):
        currentX = self.position[0]
        currentY = self.position[1]
        targetX = self.target_pos[0]
        targetY = self.target_pos[1]
        # create a box around the destination, if Unit enters the box it stops updating
        if not is_within_box((currentX, currentY), get_collision_points((targetX, targetY), (100, 100))):
            self.path = Unit_AI.a_star(self.current_node, get_closest_node(self.target_pos, grid), grid)
        else:
            self.target_pos =self.position



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

        scale = camera(self.IMAGE_SCALE)
        img = self.IMAGE
        dimensions = (img.get_width()*scale, img.get_height()*scale)
        new_pos = camera(self.position[0], self.position[1])
        if sum(dimensions) < self.SIMPLIFY_AT * min(camera.screen.get_size()) / camera.default_screen_size:
            self.DRAW_SHAPE(camera.screen,
                            GlobalVariables.TEAM_COLORS[self.team],
                            new_pos,
                            max(dimensions) * self.SHAPE_SIZE_ADJUST)
            return

        super(Unit, self).draw(camera)






