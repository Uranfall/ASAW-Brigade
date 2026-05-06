import pygame
from Node import Node
from shared_utility import get_closest_node
from EntityProps import MouseTail
from UnitClass import Unit
from graphics.graphics_utility import Camera


class Mouse(Unit):

    IMAGE = pygame.image.load('Sprites/Units/mouse_no_tail.png')
    IMAGE_ROTATION = 90
    IMAGE_SCALE = 0.75
    RENDER_LAYER = 4

    def __init__(self, position: tuple[int, int], rotation: float, selected: bool, team: int):
        super().__init__(position, rotation, selected)
        self.current_node = None
        self.team = team
        self.speed = 2
        self.hp = 10
        self.damage = 3
        self.attackRange = 100
        self.attackTickSpeed = 20
        self.tail = MouseTail((0, -70), 180+rotation, self)

    def draw(self, camera: Camera):
        self.tail.draw(camera)
        super().draw(camera)


class Soldier(Unit):
    IMAGE = pygame.image.load('Sprites/Units/soldier.png')
    IMAGE_ROTATION = 90
    IMAGE_SCALE = 0.3

    def __init__(self, position: tuple[int, int], rotation: float, selected: bool, team: int):
        super().__init__(position, rotation, selected)
        self.current_node = None
        self.team = team
        self.speed = 1
        self.hp = 30
        self.damage = 2
        self.attackRange = 500
        self.attackTickSpeed = 30

