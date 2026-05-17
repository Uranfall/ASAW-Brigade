import pygame.image

from Entity import Entity


class Burrito(Entity):
    IMAGE = pygame.image.load('Sprites/Objects/burrito_turkeysausage.png')
    IMAGE_SCALE = 0.25


class WoodenBox(Entity):
    IMAGE = pygame.image.load('Sprites/Objects/woodentexture.jpg')
    IMAGE_SCALE = 0.25


class Barrel(Entity):
    IMAGE = pygame.image.load('Sprites/Objects/NEFt.png')
    IMAGE_SCALE = 0.75
