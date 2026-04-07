from __future__ import annotations  # So we can reference the class in itself.
from os import PathLike

import pygame

from graphics.graphics_utility import Camera


class Entity:
    IMAGE: pygame.image = pygame.image.load("./Sprites/PlaceHolders/place_holder.png")
    IMAGE_ROTATION = 0.0
    IMAGE_SCALE = 0.3
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
        scale = camera(self.IMAGE_SCALE)
        img = self.IMAGE
        dimensions = (img.get_width()*scale, img.get_height()*scale)
        new_pos = camera(self.position[0], self.position[1])
        corner = (new_pos[0] - dimensions[0]/2, new_pos[1] - dimensions[1]/2)

        # start: Check if entity should be visible on screen. If the entity is outside the screen, don't draw.
        if not (-dimensions[0] < corner[0] < camera.screen.get_width()+dimensions[0] and
                -dimensions[1] < corner[1] < camera.screen.get_height()+dimensions[1]):  # Can't use is_within_box here.
            return
        # end: Check if entity should be visible on screen.

        # start: Check the size of the entity. If the entity is smaller than a certain threshold, draw a circle instead.
        if sum(dimensions) < self.SIMPLIFY_AT*min(camera.screen.get_size())/camera.default_screen_size:
            self.DRAW_SHAPE(camera.screen, self.COLOR, new_pos, max(dimensions)*self.SHAPE_SIZE_ADJUST)
            return
        # end: Check the size of teh entity.

        # start: Apply transformations to image.
        img = pygame.transform.rotozoom(img, self.rotation+self.IMAGE_ROTATION, scale)
        corner2 = (new_pos[0] - img.get_width() / 2, new_pos[1] - img.get_height() / 2)
        corner2 = img.get_rect(center=img.get_rect(topleft=corner2).center)
        # end: Apply transformations to image.

        camera.screen.blit(img, corner2)  # Put the image onto the screen.
