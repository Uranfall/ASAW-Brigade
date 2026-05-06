from __future__ import annotations

import random
from operator import truediv

import pygame
from logic_utility import *
import GlobalVariables
import Unit_AI
from Node import Node
from shared_utility import *
from Entity import Entity
from graphics.graphics_utility import Camera


def shot_fired():
    r1 = random.randint(1,100)
    if r1>30:
        return True
    else:
        return False


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
        self.current_node = Node
        self.target_node = self.current_node
        self.path = []
        self.target_pos = position
        self.target_rotation = rotation

        self.hp = 10
        self.damage = 2
        self.attackRange = 100
        self.team = 0
        self.targetUnit = None
        self.selected = selected
        self.speed = 1


    def set_position(self, position: tuple[int, int]):
        self.position = position
    def get_position(self):
        return list(self.position)

    def get_attack_box(self):
        return [self.position[0]-self.attackRange, self.position[1]-self.attackRange, self.position[0]+self.attackRange, self.position[1]+self.attackRange]
    def get_collision_points(self):
        scale = self.IMAGE_SCALE
        img = self.IMAGE
        dimensions = (img.get_width() * scale, img.get_height() * scale)
        return get_collision_points(self.position, dimensions)


    def calc_rotation(self):
        #for self: when we add unit targeting, check if enemy is in range
        targetX = self.target_node.x - self.position[0]
        targetY = self.target_node.y - self.position[1]
        self.rotation = vector_to_angle((targetX, targetY))

    def move(self, targetX,targetY):
        currentX = self.position[0]
        currentY = self.position[1]
        if not is_within_box((currentX, currentY), get_collision_points((targetX, targetY), (100, 100))):
            dx, dy = (targetX - currentX, targetY - currentY)
            stepX, stepY = (self.speed*dx/60, self.speed*dy/60)
            self.position = (currentX+stepX, currentY+stepY)

    def calc_movement(self, grid):
        currentX = self.position[0]
        currentY = self.position[1]
        targetX = self.target_pos[0]
        targetY = self.target_pos[1]
        # create a box around the destination, if Unit enters the box it stops updating
        if not is_within_box((currentX, currentY), get_collision_points((targetX, targetY), (100, 100))):
            if self.target_node!=self.current_node:
                print("ddd")
                if not self.path:
                    print("aaa")
                    print("1.", self.current_node.x,self.current_node.y, "2.", get_closest_node(self.target_pos, grid).x,get_closest_node(self.target_pos, grid).y)
                    self.path = Unit_AI.a_star(self.current_node, get_closest_node(self.target_pos, grid), grid)
                    for node in self.path:
                        print(node.x,node.y)
                    current = self.path[0]
                    self.target_node = current
                    self.path.remove(current)

                if currentX != self.target_node and currentY == self.target_node:
                    print("bbb")
                    self.move(self.target_node.x, self.target_node.y)
                else:
                    print("ccc")
                    current = self.path[0]
                    self.target_node = current
                    self.path.remove(current)
                    self.path = shift_list_left(self.path)
            else:
                self.move(targetX, targetY)



        else:
            self.target_pos = self.position
            self.target_node = self.current_node
            self.path = []



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






