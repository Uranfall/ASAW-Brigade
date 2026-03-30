from __future__ import annotations  # So we can reference the class in itself.
from os import PathLike

import pygame


class Entity:
    #seeThrough - Boolean that checks if you can see through the entity or not, used for ray logic
    #collision - if a unit can go through the object or not
    def __init__(self,
                 position: tuple[int, int],
                 rotation: float,
                 image: PathLike = "./Sprites/PlaceHolders/place_holder.png",
                 see_through=False,
                 collision=True):
        self.position = position
        self.rotation = rotation
        self.collision_points = []
        self.image: PathLike = image
        self.see_through = see_through
        self.collision = collision

    def is_colliding_with(self, entity: Entity) -> bool:
        ...

    def does_ray_intersect(self, ray_position, ray_rotation: float) -> bool:
        ...
    
    def game_tick(self, game_state):  # for any object which needs to be updates, checks the game tick and then checks if there were any updates
        pass

    def draw(self, screen: pygame.display):
        img = pygame.image.load(self.image)
        img = pygame.transform.rotate(img, self.rotation)
        img = pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))
        screen.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))
