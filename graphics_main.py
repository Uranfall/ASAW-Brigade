from typing import Sequence

import pygame

from Entity import Entity
from Unit import Unit
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

        self.selection_box_start = (0, 0)
        self.delta_time = 0

    def get_selection_box_in_screen(self):
        start, end = self.selection_box_start, self.mouse_pos
        return min(start[0], end[0]), min(start[1], end[1]), *map(lambda vals: max(vals)-min(vals), zip(start, end))

    def get_selection_box(self):
        start, end = self.camera.screen_to_global(*self.selection_box_start),\
                     self.camera.screen_to_global(*self.mouse_pos)
        return min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]), max(start[1], end[1])


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
    ui_data.delta_time = 1/ui_data.clock.tick(60)
    out = UITickOut()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            out.run = False
            return out
        if event.type == pygame.MOUSEWHEEL:
            ui_data.camera.adjust_zoom(event.y, pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ui_data.selection_box_start = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[1]:
        mouse_since_grabbing = pygame.mouse.get_pos()
        ui_data.camera.adjust_position([ui_data.mouse_pos[0] - mouse_since_grabbing[0],
                                        ui_data.mouse_pos[1] - mouse_since_grabbing[1]])
    else:
        ui_data.camera.apply()
        ui_data.mouse_pos = pygame.mouse.get_pos()

    pygame.draw.circle(ui_data.screen,
                       (255, 0, 0),
                       ui_data.camera(250, 0),
                       int(ui_data.camera(40)),
                       int(ui_data.camera(5)))

    selection_box = ui_data.get_selection_box()
    for entity in entities:
        entity.draw(ui_data.camera)
        if pygame.mouse.get_pressed()[0] and isinstance(entity, Unit):
            if selection_box[0] <= entity.position[0] <= selection_box[2] and \
                    selection_box[1] <= entity.position[1] <= selection_box[3]:
                entity.selected = True
            elif not (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                entity.selected = False
    if pygame.mouse.get_pressed()[0]:
        pygame.draw.rect(ui_data.screen, (20, 20, 255), ui_data.get_selection_box_in_screen(), 2)

    if pygame.key.get_pressed()[pygame.K_w]:
        ui_data.camera.position[1] += 100*ui_data.delta_time/ui_data.camera.zoom
    if pygame.key.get_pressed()[pygame.K_s]:
        ui_data.camera.position[1] -= 100*ui_data.delta_time/ui_data.camera.zoom
    if pygame.key.get_pressed()[pygame.K_d]:
        ui_data.camera.position[0] += 100*ui_data.delta_time/ui_data.camera.zoom
    if pygame.key.get_pressed()[pygame.K_a]:
        ui_data.camera.position[0] -= 100*ui_data.delta_time/ui_data.camera.zoom

    text_surface = FONT.render(str(ui_data.clock.get_fps()), False, (0, 0, 0))
    ui_data.screen.blit(text_surface, (0, 0))

    pygame.display.update()
    ui_data.screen.fill((10, 100, 10))
    return out

