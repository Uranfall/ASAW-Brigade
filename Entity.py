from __future__ import annotations  # So we can reference the class in itself.
from os import PathLike

import pygame

from graphics_utility import Camera


class Entity:
    IMAGE: PathLike = "./Sprites/PlaceHolders/place_holder.png"
    IMAGE_SCALE = 0.5

    #seeThrough - Boolean that checks if you can see through the entity or not, used for ray logic
    #collision - if a unit can go through the object or not
    def __init__(self,
                 position: tuple[int, int],
                 rotation: float,
                 see_through=False,
                 collision=True):
        self.position = position
        self.rotation = rotation
        self.collision_points = []
        self.see_through = see_through
        self.collision = collision

    def is_colliding_with(self, entity: Entity) -> bool:
        ...

    def does_ray_intersect(self, ray_position, ray_rotation: float) -> bool:
        ...
    
    def game_tick(self, game_state):  # for any object which needs to be updates, checks the game tick and then checks if there were any updates
        pass

    def draw(self, screen: pygame.display, camera: Camera):
        scale = camera(self.__class__.IMAGE_SCALE)
        img = pygame.image.load(self.__class__.IMAGE)
        dimensions = (img.get_width()*scale, img.get_height()*scale)
        img = pygame.transform.rotate(img, self.rotation)
        img = pygame.transform.scale(img, dimensions)
        new_pos = camera(self.position[0], self.position[1])
        screen.blit(img, (new_pos[0] - dimensions[0]/2, new_pos[1] - dimensions[1]/2))
