import random

import pygame

import DebugGlobal
from Entities.Units import Mouse
from Unit_AI import a_star
from logic_utility import get_closest_node
from VFX import Explosion
from graphics.Debug_Entities import DebugRay, DebugLine
from UnitClass import Unit
from Entity import Entity
from graphics.Ground import Ground
from graphics.graphics_main import UIData, ui_tick
from logic_main import logic_tick, create_grid, get_current_node
from map import map_info


def main():
    #path = a_star(start, goal, grid) for when you finish playing deadlock: this is for creating the path

    ui_data = UIData(pygame.display.set_mode((500, 500), pygame.RESIZABLE))
    DebugGlobal.ui_data = ui_data
    player_team = 0
    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    map_objects, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE = map_info()

    units: list[Unit] = [Mouse((0, 0), 0, 1, False),]\
               + [Mouse((random.randint(-20000, 20000), random.randint(-10000, 10000)),
                       random.randint(0, 360), 1, False) for _ in range(100)]
    entities: list[Entity] = units + map_objects

    for unit in units:
        unit.current_node = get_current_node(unit.get_position(), grid)

    run = True
    while run:
        entities[0].rotation += 45*ui_data.delta_time
        ui_out = ui_tick(ui_data, entities, units, grid, GRID_SIZE)
        logic_tick(entities, units, grid)
        run = ui_out.run


if __name__ == '__main__':
    main()