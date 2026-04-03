from __future__ import annotations  # So we can reference the class in itself.
from os import PathLike

import pygame

from graphics_utility import Camera


class Entity:
    IMAGE: pygame.image = pygame.image.load("./Sprites/PlaceHolders/place_holder.png")
    IMAGE_SCALE = 0.5
    COLOR = (100, 100, 70)
    SIMPLIFY_AT = 25  # Draw a simple shape instead of the image if smaller than.
    DRAW_SHAPE: pygame.draw = pygame.draw.circle
    SHAPE_SIZE_ADJUST = 0.25

    #seeThrough - Boolean that checks if you can see through the entity or not, used for ray logic
    #collision - if a unit can go through the object or not
    def __init__(self,
                 position: tuple[int, int],
                 rotation: float,
                 see_through=False,
                 selected=False,
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

    def draw(self, camera: Camera):
        scale = camera(self.__class__.IMAGE_SCALE)
        img = self.__class__.IMAGE

        dimensions = (img.get_width()*scale, img.get_height()*scale)

        new_pos = camera(self.position[0], self.position[1])
        corner = (new_pos[0] - dimensions[0]/2, new_pos[1] - dimensions[1]/2)
        if not (-dimensions[0] < corner[0] < camera.screen.get_width()+dimensions[0] and
                -dimensions[1] < corner[1] < camera.screen.get_height()+dimensions[1]):
            return

        if sum(dimensions) < self.__class__.SIMPLIFY_AT*min(camera.screen.get_size())/camera.default_screen_size:
            self.DRAW_SHAPE(camera.screen, self.__class__.COLOR, new_pos, max(dimensions)*self.__class__.SHAPE_SIZE_ADJUST)
            return

        img = pygame.transform.scale(img, dimensions)
        img = pygame.transform.rotate(img, self.rotation)
        corner2 = (new_pos[0] - img.get_width() / 2, new_pos[1] - img.get_height() / 2)
        corner2 = tuple(map(round, img.get_rect(center=img.get_rect(topleft=corner2).center)))

        camera.screen.blit(img, corner2)
