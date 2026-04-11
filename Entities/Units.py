import pygame

from EntityProps import MouseTail
from UnitClass import Unit
from graphics.graphics_utility import Camera


class Mouse(Unit):

    IMAGE = pygame.image.load('Sprites/Units/mouse_no_tail.png')
    IMAGE_ROTATION = 90
    IMAGE_SCALE = 0.75
    RENDER_LAYER = 4

    def __init__(self, position: tuple[int, int], rotation: float, speed: int, selected: bool):
        super().__init__(position, rotation, speed, selected)
        self.tail = MouseTail((0, -70), 180+rotation, self)

    def draw(self, camera: Camera):
        self.tail.draw(camera)
        super().draw(camera)


class Soldier(Unit):
    IMAGE = pygame.image.load('Sprites/Units/soldier.png')
    IMAGE_ROTATION = 90
    IMAGE_SCALE = 0.3

