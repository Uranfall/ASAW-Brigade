import math
import time

import pygame.draw

from Entity import Entity
from GlobalVariables import FONT, TEXT_RED_CURVE
from graphics.graphics_utility import Camera
from shared_utility import ValueCurve, get_collision_points, is_within_box, lerp
from typing import Callable


class UIEntity(Entity):
    LIFETIME = 5
    RENDER_LAYER = 10
    TRIGGERABLE = True

    def __init__(self, position: tuple[int, int], rotation: float, time_offset=0.0):
        super().__init__(position, rotation)
        self.creation_time = time.time()+time_offset
        self.collision = False

    def get_age(self):
        return time.time()-self.creation_time

    def get_progress(self):
        return self.get_age()/self.LIFETIME


class Text(UIEntity):
    LIFETIME = 1

    def __init__(self, position: tuple[int, int],
                 rotation: float,
                 text: str,
                 color: tuple[int, int, int] | ValueCurve,
                 size=30.0,
                 time_offset=0.0,
                 font_name='OCR A Extended',
                 bold=False,
                 italic=False):
        super().__init__(position, rotation, time_offset)
        self.text = text
        self.color = color
        self.size = size
        self.font_name = font_name
        self.bold = bold
        self.italic = italic

    def draw(self, camera: Camera):
        if isinstance(self.color, ValueCurve):
            color = self.color(self.get_progress())
        else:
            color = self.color
        font = pygame.font.SysFont(self.font_name, int(camera(self.size)), self.bold, self.italic)
        text_surface = font.render(self.text, True, color)
        rect = text_surface.get_rect(center=camera(*self.position))
        camera.screen.blit(text_surface, rect)


class Button(UIEntity):
    def __init__(self,
                 position: tuple[int, int],
                 scale: tuple[float, float],
                 text: Text,
                 action: Callable = None,
                 border_color=(50, 50, 60),
                 color=ValueCurve(((30, 30, 30), 0), ((100, 40, 45), 1))):
        super().__init__(position, 0)
        self.scale = scale
        self.text = text
        self.text.position = (self.text.position[0]+self.position[0], self.text.position[1]+self.position[1])
        self.color = color
        self.border_color = border_color
        self.hovering_time = time.time()
        self.not_hover_time = time.time()
        self.hover_animation_duration = 0.5
        self.action = action

    def update_hover(self, camera: Camera):
        global_mouse = camera.screen_to_global(*pygame.mouse.get_pos())
        box = get_collision_points(self.position, self.scale)
        if not is_within_box(global_mouse, box):
            self.hovering_time = time.time()
            return False
        self.not_hover_time = time.time()
        return True

    def draw(self, camera: Camera):
        is_hover = self.update_hover(camera)
        if is_hover:
            color = self.color((time.time() - self.hovering_time) / self.hover_animation_duration)
        else:
            color = self.color(1 - (time.time() - self.not_hover_time) / self.hover_animation_duration)
        pygame.draw.rect(camera.screen,
                         color,
                         (*camera(self.position[0]-self.scale[0]/2, self.position[1]+self.scale[1]/2),
                          self.scale[0]*camera.get_zoom(), self.scale[1]*camera.get_zoom()),
                         border_radius=round(camera(10)),)

        pygame.draw.rect(camera.screen,
                         self.border_color,
                         (*camera(self.position[0]-self.scale[0]/2, self.position[1]+self.scale[1]/2),
                          self.scale[0]*camera.get_zoom(), self.scale[1]*camera.get_zoom()),
                         math.ceil(camera(3 if is_hover and pygame.mouse.get_pressed()[0] else 7)),
                         border_radius=round(camera(10)),)
        self.text.creation_time = self.creation_time

        self.text.draw(camera)


class TextBox(Button):
    def __init__(self, position: tuple[int, int], scale: tuple[float, float], max_length: int, default_text=''):
        super().__init__(position, scale, Text((0, 0), 0, default_text, TEXT_RED_CURVE))
        self.max_length = max_length
        self.selected = False
        self.action = self.select
        self.default_text = default_text
        self.empty = True

    def select(self):
        self.selected = True

    def key_down(self, key: str):
        if self.selected:
            if key == '\x08':
                if not self.empty:
                    self.text.text = self.text.text[:-1]
                    if self.text.text == '':
                        self.empty = True
                        self.text.text = self.default_text
            elif len(self.text.text) < self.max_length:
                if self.empty:
                    self.text.text = ''
                self.empty = False
                self.text.text += key


class RotatingGear1(UIEntity):
    IMAGE = pygame.image.load('Sprites/ui/gear_gray.png')
    IMAGE_SCALE = 1.25
    LIFETIME = 1
    TRIGGERABLE = False

    def __init__(self, position: tuple[int, int], rotation: float, torque: float = 1.0):
        super().__init__(position, rotation)
        self.torque = torque
        self.start_rotation = rotation

    def draw(self, camera: Camera):
        super().draw(camera)
        before_rotation = self.rotation
        self.rotation = lerp(self.start_rotation,
                             self.start_rotation+self.torque,
                             self.get_progress())


class RotatingGear2(RotatingGear1):
    IMAGE_SCALE = 0.8


class ExpandingCircle(UIEntity):
    COLOR = (50, 50, 255)
    LIFETIME = 0.25
    FINAL_SIZE = 20

    def __init__(self, position: tuple[int, int], time_offset=0.0):
        super().__init__(position, 0, time_offset)

    def draw(self, camera: Camera):
        pygame.draw.circle(camera.screen,
                           self.COLOR,
                           camera(*self.position),
                           math.ceil(camera(self.FINAL_SIZE*self.get_progress())),
                           math.ceil(camera(2)))
