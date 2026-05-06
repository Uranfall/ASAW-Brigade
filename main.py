import random

import pygame

import DebugGlobal
from Entities.Units import *
from GlobalVariables import TEXT_RED_CURVE
from Unit_AI import a_star
from graphics.UI_Entities import Button, Text
from shared_utility import get_closest_node
from VFX import Explosion
from graphics.Debug_Entities import DebugRay, DebugLine
from UnitClass import Unit
from Entity import Entity
from graphics.Ground import Ground
from graphics.graphics_main import UIData, ui_tick
from logic_main import logic_tick, create_grid, LOGIC_DATA
from shared_utility import get_closest_node
from map import map_info
from GameData import GameDataLocal


def main(screen=pygame.display.set_mode((500, 500), pygame.RESIZABLE)):
    #path = a_star(start, goal, grid) for when you finish playing deadlock: this is for creating the path

    def quit_main():
        nonlocal run
        run = False


    def create_mouse():
        spawn_points = game_data.get_player_spawns(player_team)
        money = game_data.get_player_currency(player_team)
        if money >= 500:
            game_data.update_player_currency(-500, player_team)
            newUnit = Mouse(spawn_points[0], 90, False, player_team)
            newUnit.current_node = get_closest_node(newUnit.get_position(), game_data.get_grid())
            newUnit.target_node = newUnit.current_node
            # add unit
            units.append(newUnit)
            entities.append(newUnit)
            # shift list left, set the next spawn as the one the next unit is going to use
            game_data.shift_player_spawns(player_team)




    def create_soldier():
        spawn_points = game_data.get_player_spawns(player_team)
        money = game_data.get_player_currency(player_team)
        if money >= 500:
            game_data.update_player_currency(-500, player_team)
            newUnit = Soldier(spawn_points[0], 90, False, player_team)
            newUnit.current_node = get_closest_node(newUnit.get_position(), game_data.get_grid())
            newUnit.target_node = newUnit.current_node
            # add unit
            units.append(newUnit)
            entities.append(newUnit)
            # shift list left, set the next spawn as the one the next unit is going to use
            game_data.shift_player_spawns(player_team)


    def create_uuuhh_idk____oh_wait_tank__right():
        pass

    ui_data = UIData(screen)
    exit_button = Button((0, 220), (100, 40), Text((0, 0), 0, 'Quit', TEXT_RED_CURVE), action=quit_main)
    exit_button.creation_time = 0
    ui_data.add_on_screen_entity(exit_button)
    c_b1 = Button((-130, -220), (100, 40), Text((0, 0), 0, 'Mouse', TEXT_RED_CURVE, size=30), action=create_mouse)
    c_b2 = Button((0, -220), (140, 40), Text((0, 0), 0, 'Soldier', TEXT_RED_CURVE, size=30), action=create_soldier)
    c_b3 = Button((130, -220), (100, 40), Text((0, 0), 0, 'Tank', TEXT_RED_CURVE, size=30),
                  action=create_uuuhh_idk____oh_wait_tank__right)
    ui_data.add_on_screen_entity(c_b1)
    ui_data.add_on_screen_entity(c_b2)
    ui_data.add_on_screen_entity(c_b3)
    ui_data.add_on_screen_entity(Text((0, -180), 0, 'Creation Menu:', TEXT_RED_CURVE))

    logic_data = LOGIC_DATA()
    DebugGlobal.ui_data = ui_data
    player_team = 1

    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    map_objects, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE = map_info()

    units: list[Unit] = [Mouse((0, 0), 90, 1, 0),]\
               + [Mouse((random.randint(-2000, 2000), random.randint(-2000, 2000)),
                       random.randint(0, 360), False, random.randint(0, 1)) for _ in range(10)]
    entities: list[Entity] = units + map_objects

    for unit in units:
        unit.team = random.randint(0, 1)
        unit.current_node = get_closest_node(unit.get_position(), grid)
        unit.target_node = unit.current_node
    game_data = GameDataLocal(entities, units, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE)

    run = True
    while run:
        entities[0].rotation += 45*ui_data.delta_time
        ui_out = ui_tick(ui_data, game_data)
        logic_tick(entities, units, grid, logic_data, game_data)
        run = run and ui_out.run


if __name__ == '__main__':
    main()