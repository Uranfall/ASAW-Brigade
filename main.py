import random

import pygame

import DebugGlobal
from Entities.Units import Mouse
from Unit_AI import a_star
from shared_utility import get_closest_node
from VFX import Explosion
from graphics.Debug_Entities import DebugRay, DebugLine
from UnitClass import Unit
from Entity import Entity
from graphics.Ground import Ground
from graphics.graphics_main import UIData, ui_tick
from logic_main import logic_tick, create_grid, get_current_node
from map import map_info
from GameData import GameDataLocal


def main(screen=pygame.display.set_mode((500, 500), pygame.RESIZABLE)):
    #path = a_star(start, goal, grid) for when you finish playing deadlock: this is for creating the path

    ui_data = UIData(screen)
    DebugGlobal.ui_data = ui_data
    player_team = 0
    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    map_objects, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE = map_info()

    units: list[Unit] = [Mouse((0, 0), 90, 1, False),]\
               + [Mouse((random.randint(-2000, 2000), random.randint(-2000, 2000)),
                       random.randint(0, 360), 1, False) for _ in range(10)]
    entities: list[Entity] = units + map_objects

    for unit in units:
        unit.current_node = get_current_node(unit, grid)
        unit.target_node = unit.current_node


    game_data = GameDataLocal(entities, units, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE)

    run = True
    while run:
        entities[0].rotation += 45*ui_data.delta_time
        ui_out = ui_tick(ui_data, game_data)
        logic_tick(entities, units, grid)
        run = ui_out.run


if __name__ == '__main__':
    main()