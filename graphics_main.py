from typing import Sequence

import pygame

from Entity import Entity
from graphics_utility import Camera

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 30)


class UIData:
    def __init__(self,
                 screen: pygame.display,
                 camera: Camera = None,
                 clock: pygame.time.Clock = None,
                 mouse_pos: list[int, int] = None):
        if camera is None:
            camera = Camera([0, 0], 1, screen)
        self.camera = camera
        if clock is None:
            clock = pygame.time.Clock()
        self.clock = clock
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = mouse_pos
        self.screen = screen


class UITickOut:
    """
    Variables:
    "run" - Set to true by default, turns false if user tries to exit.
    """
    def __init__(self):
        self.run = True


def ui_tick(ui_data: UIData, entities: Sequence[Entity]) -> UITickOut:
    """
    Shows everything that needs to be shown, and outputs commands from user.
    """
    out = UITickOut()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            out.run = False
            return out
        if event.type == pygame.MOUSEWHEEL:
            ui_data.camera.adjust_zoom(event.y, pygame.mouse.get_pos())

    if pygame.mouse.get_pressed()[1]:
        new_mouse = pygame.mouse.get_pos()
        ui_data.camera.adjust_position([ui_data.mouse_pos[0] - new_mouse[0], ui_data.mouse_pos[1] - new_mouse[1]])
    else:
        ui_data.camera.apply()
        ui_data.mouse_pos = pygame.mouse.get_pos()

    pygame.draw.circle(ui_data.screen,
                       (255, 0, 0),
                       ui_data.camera(250, 0),
                       int(ui_data.camera(40)),
                       int(ui_data.camera(5)))
    for entity in entities:
        entity.draw(ui_data.screen, ui_data.camera)

    text_surface = FONT.render(str(ui_data.clock.get_fps()), False, (0, 0, 0))
    ui_data.screen.blit(text_surface, (0, 0))

    pygame.display.update()
    ui_data.screen.fill((10, 100, 10))
    ui_data.clock.tick(60)
    return out

