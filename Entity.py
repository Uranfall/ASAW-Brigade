from __future__ import annotations  # So we can reference the class in itself.
from os import PathLike

import pygame

from graphics_utility import Camera


class Entity:
    IMAGE: pygame.image = pygame.image.load("./Sprites/PlaceHolders/place_holder.png")
    IMAGE_SCALE = 0.5
    COLOR = (100, 100, 70)
    SIMPLIFY_AT = 40  # Draw a simple shape instead of the image if smaller than.
    DRAW_SHAPE: pygame.draw = pygame.draw.circle
    SHAPE_SIZE_ADJUST = 0.3
    STATIC_ROTATION = True

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

        # The following variables are only for graphics.
        self.zoom_render: tuple[float, pygame.image] | None = None
        self.rotated_picture = pygame.transform.rotate(self.__class__.IMAGE, self.rotation) \
            if self.__class__.STATIC_ROTATION else None

    def is_colliding_with(self, entity: Entity) -> bool:
        ...

    def does_ray_intersect(self, ray_position, ray_rotation: float) -> bool:
        ...
    
    def game_tick(self, game_state):  # for any object which needs to be updates, checks the game tick and then checks if there were any updates
        pass

    def draw(self, screen: pygame.display, camera: Camera):
        scale = camera(self.__class__.IMAGE_SCALE)
        img = self.__class__.IMAGE

        dimensions = (img.get_width()*scale, img.get_height()*scale)
        new_pos = camera(self.position[0], self.position[1])
        if sum(dimensions) < self.__class__.SIMPLIFY_AT:
            self.DRAW_SHAPE(screen, self.__class__.COLOR, new_pos, max(dimensions)*self.__class__.SHAPE_SIZE_ADJUST)
            return

        corner = (new_pos[0] - dimensions[0]/2, new_pos[1] - dimensions[1]/2)
        if not (-dimensions[0] < corner[0] < screen.get_width()+dimensions[0] and
                -dimensions[1] < corner[1] < screen.get_height()+dimensions[1]):
            return

        if self.rotated_picture is None:
            img = pygame.transform.rotate(img, self.rotation)
        else:
            img = self.rotated_picture
        if self.zoom_render is not None\
                and camera.get_zoom() == self.zoom_render[0]:
            img = self.zoom_render[1]
        else:
            img = pygame.transform.scale(img, dimensions)
            self.zoom_render = (camera.get_zoom(), img)
        screen.blit(img, corner)
