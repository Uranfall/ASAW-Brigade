import pygame
from Node import Node
from VFX import Explosion, GunFire, SmokeTrail
from shared_utility import get_closest_node
from EntityProps import MouseTail
from UnitClass import Unit
from graphics.graphics_utility import Camera


class Mouse(Unit):
    NAME = 'MO'

    IMAGE = pygame.image.load('Sprites/Units/mouse_no_tail.png')
    IMAGE_ROTATION = 90
    IMAGE_SCALE = 0.75
    RENDER_LAYER = 4

    def __init__(self, position: tuple[int, int], rotation: float, selected: bool = False, team: int = 0):
        super().__init__(position, rotation, selected)
        self.current_node = None
        self.team = team
        self.speed = 0.75
        self.hp = 20
        self.damage = 3
        self.attackRange = 150
        self.attackTickSpeed = 20
        self.tail = MouseTail((0, -70), 180+rotation, self)

    def draw(self, camera: Camera):
        self.tail.draw(camera)
        super().draw(camera)


class Soldier(Unit):
    NAME = 'SO'

    IMAGE = pygame.image.load('Sprites/Units/soldier.png')
    IMAGE_ROTATION = 90
    IMAGE_SCALE = 0.3

    def __init__(self, position: tuple[int, int], rotation: float, selected: bool = False, team: int = 0):
        super().__init__(position, rotation, selected)
        self.current_node = None
        self.team = team
        self.speed = 0.5
        self.hp = 50
        self.damage = 2
        self.hitChance = 20
        self.attackRange = 1000
        self.attackTickSpeed = 10


class Tank(Unit):
    NAME = "TA"

    SHOOTING_EFFECTS = [SmokeTrail, GunFire]
    IMAGE = pygame.image.load('Sprites/Units/tank merkava.png')
    IMAGE_ROTATION = 90
    IMAGE_SCALE = 1
    DEATH_EFFECTS = [Explosion]
    MUZZLE_DISTANCE = 100

    def __init__(self, position: tuple[int, int], rotation: float, selected: bool = False, team: int = 0):
        super().__init__(position, rotation, selected)
        self.current_node = None
        self.team = team
        self.speed = 0.25
        self.hp = 150
        self.damage = 50
        self.hitChance = 60
        self.attackRange = 1000
        self.attackTickSpeed = 60

