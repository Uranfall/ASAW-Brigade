import math

import pygame.draw

import shared_utility
from Entity import Entity
from graphics.UI_Entities import UIEntity
from graphics.graphics_utility import Camera


class DebugEntity(UIEntity):
    LIFETIME = 0.1

    def __init__(self, position: tuple[int, int], rotation: float, stay_alive_for=float('inf')):
        super().__init__(position, rotation, stay_alive_for)

    pass


class DebugRay(DebugEntity):
    def __init__(self, position: tuple[int, int],
                 rotation: float,
                 distance: float,
                 width=10.0,
                 stay_alive_for=float('inf')):
        super().__init__(position, rotation, stay_alive_for)
        self.distance = distance
        self.width = width

    def draw(self, camera: Camera):
        direction = shared_utility.angle_to_vector(self.rotation, distance=self.distance)
        ray_end = (self.position[0]+direction[0], self.position[1]+direction[1])
        new_pos = camera(*self.position)
        new_end = camera(*ray_end)
        pygame.draw.line(camera.screen, (50, 255, 50), new_pos, new_end, int(camera(self.width)))


class DebugLine(DebugEntity):
    def __init__(self, pos1: tuple[float, float],
                 pos2: tuple[float, float],
                 width=10.0,
                 color=(0, 0, 255),
                 stay_alive_for=float('inf')):
        super().__init__((0, 0), 0, stay_alive_for)
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color
        self.width = width

    def draw(self, camera: Camera):
        pygame.draw.line(camera.screen,
                         self.color,
                         camera(*self.pos1),
                         camera(*self.pos2),
                         math.ceil(camera(self.width)))


class DebugBox(DebugEntity):
    def __init__(self,
                 pos: tuple[float, float, float, float],
                 width=10.0,
                 color=(0, 0, 255),
                 stay_alive_for=float('inf')):
        super().__init__((0, 0), 0, stay_alive_for)
        pos = (*sorted([pos[0], pos[2]]), *reversed(sorted([pos[1], pos[3]])))
        pos = pos[0], pos[2], pos[1], pos[3]
        self.pos = pos[:2]
        self.size = pos[2]-pos[0], pos[1]-pos[3]
        self.color = color
        self.width = width

    def draw(self, camera: Camera):
        pygame.draw.rect(camera.screen,
                         self.color,
                         camera(*self.pos, *self.size),
                         math.ceil(camera(self.width)))

