import math
import time
from typing import Sequence, Iterable

import pygame

from Entity import Entity
from GlobalVariables import FONT
from Protocol.Command import Command
from UnitClass import Unit
from VFX import Explosion, ColorfulExplosion
from graphics.UI_Entities import UIEntity, ExpandingCircle, TargetTriangle
from graphics.graphics_utility import Camera
from shared_utility import is_within_box, get_closest_node
from GameData import GameData


def get_selected_units(entities: Sequence[Entity]) -> Iterable:
    return filter(lambda entity: isinstance(entity, Unit) and entity.selected, entities)


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
        self.previous_frame = time.time()

        self.ui_entities: list[UIEntity] = []

        self.input_checks = []

    def add_on_screen_entity(self, entity: UIEntity,):
        self.input_checks.extend(entity.get_checks())
        self.camera.linked_entities.append(entity)

    def start_new_frame(self, fps=60.0):
        self.clock.tick(fps)
        self.delta_time = time.time()-self.previous_frame
        self.previous_frame = time.time()

    def end_frame(self):
        text_surface = FONT.render(str(self.clock.get_fps()), False, (0, 0, 0))
        self.screen.blit(text_surface, (0, 0))
        self.camera.render()

    def get_selection_box_in_screen(self):
        """
        Outputs the coordinates of the selection box on the screen.
        The first two values are the position of the top-left corner,
        the other two values are the position of the bottom-right corner.
        """
        start, end = self.selection_box_start, self.mouse_pos
        return min(start[0], end[0]), min(start[1], end[1]), *map(lambda vals: abs(vals[0]-vals[1]), zip(start, end))

    def get_selection_box(self):
        """
        Outputs the coordinates of the selection box in the world.
        The first two values are the position of the top-left corner,
        the other two values are the position of the bottom-right corner.
        """
        start, end = self.camera.screen_to_global(*self.selection_box_start),\
                     self.camera.screen_to_global(*self.mouse_pos)
        return min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]), max(start[1], end[1])

    def update_ui_entities(self):
        for entity in self.ui_entities[:]:
            if entity.get_progress() > 1:
                self.ui_entities.remove(entity)
            entity.draw(self.camera)


class UITickOut:
    """
    Variables:
    "run" - Set to true by default, turns false if user tries to exit.
    """
    def __init__(self):
        self.run = True


def get_closest_entity_to(pos, units):
    closest = None
    for unit in units:
        if closest is None or closest[0] > math.dist(pos, unit.position):
            closest = math.dist(pos, unit.position), unit
    return closest


def handle_user_input(ui_data: UIData, game_data: GameData, out: UITickOut):
    entities = game_data.get_entities()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            out.run = False
        if event.type == pygame.MOUSEWHEEL:
            ui_data.camera.adjust_zoom(event.y, pygame.mouse.get_pos())
        #selecting units
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ui_data.selection_box_start = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = ui_data.camera.screen_to_global(*event.pos)
            closest = get_closest_entity_to(mouse_pos, game_data.get_units())
            if closest is not None and closest[0] < closest[1].IMAGE_SCALE*min(closest[1].IMAGE.get_size()):
                closest[1].selected = True

        #  this handles unit control
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            selected = tuple(get_selected_units(entities))
            if tuple(get_selected_units(entities)):
                pos = ui_data.camera.screen_to_global(*pygame.mouse.get_pos())
                target = None
                closest = get_closest_entity_to(pos, game_data.get_units())
                if closest is not None and closest[0] < closest[1].IMAGE_SCALE * min(closest[1].IMAGE.get_size()):
                    target = closest[1]
                    ui_data.ui_entities.append(TargetTriangle((target.position[0], target.position[1]+100), 0))
                else:
                    ui_data.ui_entities += [
                        ExpandingCircle(ui_data.camera.screen_to_global(*pygame.mouse.get_pos()), -0.1),
                        ExpandingCircle(ui_data.camera.screen_to_global(*pygame.mouse.get_pos())),
                        ExpandingCircle(ui_data.camera.screen_to_global(*pygame.mouse.get_pos()), 0.1),
                    ]
                for unit in selected:
                    if target is not None and target.team != unit.team:
                        game_data.add_command(Command(Command.ATTACK, str(target.id), unit.id))
                        game_data.add_command(Command(Command.GO_TO, str(pos), unit.id))
                    else:
                        game_data.add_command(Command(Command.GO_TO, str(pos), unit.id))
            else:
                game_data.add_vfx(Explosion(ui_data.camera.screen_to_global(*pygame.mouse.get_pos()), 0))

        for check in ui_data.input_checks:
            check(event)

    # start: Logic responsible for mouse gripping the ground and moving the camera.
    if pygame.mouse.get_pressed()[1]:
        mouse_since_grabbing = pygame.mouse.get_pos()
        ui_data.camera.adjust_position([ui_data.mouse_pos[0] - mouse_since_grabbing[0],
                                        ui_data.mouse_pos[1] - mouse_since_grabbing[1]])
    else:
        ui_data.camera.apply()
    # end: logic responsible for mouse gripping the ground and moving the camera.
        ui_data.mouse_pos = pygame.mouse.get_pos()  # Note that ui_data.mouse_pos only changes when middle mouse is up.

    if pygame.key.get_pressed()[pygame.K_w]:
        ui_data.camera.position[1] += 500*ui_data.delta_time/ui_data.camera.zoom
    if pygame.key.get_pressed()[pygame.K_s]:
        ui_data.camera.position[1] -= 500*ui_data.delta_time/ui_data.camera.zoom
    if pygame.key.get_pressed()[pygame.K_d]:
        ui_data.camera.position[0] += 500*ui_data.delta_time/ui_data.camera.zoom
    if pygame.key.get_pressed()[pygame.K_a]:
        ui_data.camera.position[0] -= 500*ui_data.delta_time/ui_data.camera.zoom
    return out


def go_over_entities(ui_data: UIData, game_data: GameData, out: UITickOut):
    selection_box = ui_data.get_selection_box()

    for layer in game_data.get_layers():
        for entity in layer:
            entity.draw(ui_data.camera)

            if pygame.mouse.get_pressed()[0] and isinstance(entity, Unit):
                if is_within_box(entity.position, selection_box):
                    entity.selected = True
                elif not (pygame.key.get_pressed()[pygame.K_LSHIFT] or
                          pygame.key.get_pressed()[pygame.K_RSHIFT]):
                    entity.selected = False

    ui_data.update_ui_entities()

    if pygame.mouse.get_pressed()[0]:
        pygame.draw.rect(ui_data.screen, (20, 20, 255), ui_data.get_selection_box_in_screen(), 2)
    game_data.clean_up_vfx()
    return out


def ui_tick(ui_data: UIData, game_data: GameData) -> UITickOut:
    """
    Shows everything that needs to be shown, and outputs commands from user.
    """
    out = UITickOut()

    ui_data.start_new_frame(fps=60)

    entities = game_data.get_entities()
    handle_user_input(ui_data, game_data, out)
    go_over_entities(ui_data, game_data, out)
    ui_data.end_frame()
    return out

