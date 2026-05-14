from __future__ import annotations

import random
from operator import truediv
from typing import Type

import pygame
import GlobalVariables
from Node import Node
from VFX import GunFire, BloodSplatter, SmokeTrail, ShotEffect
from shared_utility import *
from Entity import Entity
from graphics.graphics_utility import Camera


def shot_fired(hit_chance: int):
    r1 = random.randint(1,100)
    if r1>hit_chance:
        return True
    else:
        return False


class Unit(Entity):
    NAME = 'DefaultUnit'

    SHOOTING_EFFECTS: list[Type[ShotEffect]] = [GunFire]
    DEATH_EFFECTS = [BloodSplatter]
    MUZZLE_DISTANCE = 75

    MELEE = False

    def __init__(self,
                 # unit_type: str,
                 position: tuple[float, float],
                 rotation: float,
                 team: int = 0,
                 ):
        super().__init__(position, rotation)
        self.target_pos = position
        self.target_rotation = rotation
        self.selected = False
        self.change_rate = [0, 0]

        self.hp = 10
        self.damage = 2
        self.hitChance = 20 #out of 100
        self.attackRange = 200
        self.attackTickSpeed = 20
        self.team = team
        self.targetUnit = None
        self.selected = False
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
        return scale_box(get_collision_points(self.position, dimensions), self.COLLIDER_SCALE)


    def calc_rotation(self):
        #for self: when we add unit targeting, check if enemy is in range
        target = self.target_pos
        if self.targetUnit is not None:
            target = self.targetUnit.position
        targetX = target[0] - self.position[0]
        targetY = target[1] - self.position[1]
        self.rotation = vector_to_angle((targetX, targetY))

    def move(self, targetX,targetY,deltatime):
        currentX = self.position[0]
        currentY = self.position[1]
        if not is_within_box((currentX, currentY),[targetX-100, targetY-100,targetX+100, targetY+100]):
            dx, dy = (targetX - currentX, targetY - currentY)
            stepX, stepY = (self.speed*dx*deltatime, self.speed*dy*deltatime)
            self.position = (currentX+stepX, currentY+stepY)
            self.change_rate = [stepX, stepY]
        else:
            self.change_rate = [0,0]

    def calc_movement(self, grid, deltatime):
        # create a box around the destination, if Unit enters the box it stops updating
        if not is_within_box(self.position, get_collision_points(self.target_pos, (100, 100))):
            self.move(*self.target_pos, deltatime)
        else:
            self.target_pos = self.position

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

    def get_shooting_effects(self, rotation: float | None = None):
        if rotation is None:
            rotation = self.rotation
        offset = angle_to_vector(rotation, distance=self.MUZZLE_DISTANCE)
        position = self.position[0]+offset[0], self.position[1]+offset[1]
        out = []
        for effect in self.SHOOTING_EFFECTS:
            print(self.targetUnit.IMAGE_SCALE)
            out.append(effect(position,
                              rotation,
                              math.dist(self.position, self.targetUnit.position)
                              -self.targetUnit.IMAGE_SCALE*self.targetUnit.IMAGE.get_size()[0]))
        return out

    def get_death_effects(self, rotation: float | None = None):
        if rotation is None:
            rotation = self.rotation
        out = []
        for effect in self.DEATH_EFFECTS:
            out.append(effect(self.position, rotation))
        return out

    def __str__(self, close=True):
        return f'<{super().__str__(close=False)};plr{self.team}>'

