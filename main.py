import random

import pygame
import DebugGlobal
from Entities.Units import *
from GlobalVariables import TEXT_RED_CURVE
from Protocol.Command import Command
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
        game_data.add_command(Command(Command.SPAWN, Mouse.NAME, team=player_team))

    def create_soldier():
        game_data.add_command(Command(Command.SPAWN, Soldier.NAME, team=player_team))

    def create_tank():
        game_data.add_command(Command(Command.SPAWN, Tank.NAME, team=player_team))

    #Logic related code
    logic_data = LOGIC_DATA()
    player_team = 1

    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    map_objects, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE = map_info()

    units: list[Unit] = [Mouse((200, 200), 90, 1, 0), ] \
                        + [Mouse((random.randint(-2000, 2000), random.randint(-2000, 2000)),
                                 random.randint(0, 360), False, random.randint(0, 1)) for _ in range(10)]
    entities: list[Entity] = units + map_objects

    for unit in units:
        unit.team = random.randint(0, 1)
        unit.current_node = get_closest_node(unit.get_position(), grid)
        unit.target_node = unit.current_node
    game_data = GameDataLocal(entities, units, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE)

    #UI related code
    ui_data = UIData(screen)
    DebugGlobal.ui_data = ui_data
    exit_button = Button((0, 220), (100, 40), Text((0, 0), 0, 'Quit', TEXT_RED_CURVE), action=quit_main)
    player_currency = Text((120, 220), 0, str(game_data.get_player_currency(player_team))+"$", TEXT_RED_CURVE)
    exit_button.creation_time = 0
    ui_data.add_on_screen_entity(exit_button)
    c_b1 = Button((-130, -220), (100, 40), Text((0, 0), 0, 'Mouse', TEXT_RED_CURVE, size=30), action=create_mouse)
    c_b2 = Button((0, -220), (140, 40), Text((0, 0), 0, 'Soldier', TEXT_RED_CURVE, size=30), action=create_soldier)
    c_b3 = Button((130, -220), (100, 40), Text((0, 0), 0, 'Tank', TEXT_RED_CURVE, size=30),
                  action=create_tank)
    ui_data.add_on_screen_entity(c_b1)
    ui_data.add_on_screen_entity(c_b2)
    ui_data.add_on_screen_entity(c_b3)
    ui_data.add_on_screen_entity(Text((0, -180), 0, 'Creation Menu:', TEXT_RED_CURVE))
    ui_data.add_on_screen_entity(player_currency)

    run = True
    while run:
        entities[0].rotation += 45*ui_data.delta_time
        ui_out = ui_tick(ui_data, game_data)
        logic_tick(entities, units, grid, logic_data, game_data)
        player_currency.text = str(game_data.get_player_currency(player_team))+"$"
        run = run and ui_out.run


if __name__ == '__main__':
    main()