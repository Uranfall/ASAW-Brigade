import pygame.draw

import shared_utility
from Entity import Entity
from graphics.graphics_utility import Camera


class DebugEntity(Entity):
    pass


class DebugRay(DebugEntity):
    def __init__(self, position: tuple[int, int], rotation: float, distance: float, width=10.0):
        super().__init__(position, rotation)
        self.distance = distance
        self.width = width

    def draw(self, camera: Camera):
        direction = shared_utility.angle_to_vector(self.rotation, distance=self.distance)
        ray_end = (self.position[0]+direction[0], self.position[1]+direction[1])
        new_pos = camera(*self.position)
        new_end = camera(*ray_end)
        pygame.draw.line(camera.screen, (50, 255, 50), new_pos, new_end, int(camera(self.width)))


