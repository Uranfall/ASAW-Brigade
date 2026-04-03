import math
import pygame
from Entity import Entity
import Unit_AI
from graphics_utility import Camera


class Unit(Entity):

    def __init__(self,
                 # unit_type: str,
                 position: tuple[int, int],
                 rotation: float,
                 # speed: int,
                 selected: bool,
                 act_list: list = ["idle"]):
        super().__init__(position, rotation, selected)
        self.target_pos = position
        self.target_rotation = rotation
        self.selected = selected
        #self.speed = 1
        #self.unit_type = unit_type

    def draw(self, camera: Camera):
        if self.selected:
            pygame.draw.circle(camera.screen,
                               (32, 155, 255),
                               camera(*self.position),
                               int(camera(self.__class__.SHAPE_SIZE_ADJUST * max(self.__class__.IMAGE.get_size()))),
                               math.ceil(camera(5)))
        super(Unit, self).draw(camera)

    def move(self):
        ...

    def fire(self):
        ...

    def interact(self):
        ...

    def idle(self):
        ...





