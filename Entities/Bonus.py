import pygame.image

from Entity import Entity


class HandGun(Entity):
    IMAGE = pygame.transform.flip(pygame.image.load('Sprites/PlaceHolders/hand_gun.png'), True, False)


class CatGunner(Entity):
    IMAGE = pygame.image.load('Sprites/PlaceHolders/cat_gun_cool.png')
