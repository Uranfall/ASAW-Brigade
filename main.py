import random

import pygame

import DebugGlobal
from Entities.Units import Mouse
from VFX import Explosion
from graphics.Debug_Entities import DebugRay, DebugLine
from UnitClass import Unit
from Entity import Entity
from graphics.Ground import Ground
from graphics.graphics_main import UIData, ui_tick
from logic_main import logic_tick


def main():
    ui_data = UIData(pygame.display.set_mode((500, 500), pygame.RESIZABLE))
    DebugGlobal.ui_data = ui_data
    player_team = 0
    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    entities: list[Entity] = [Mouse((0, 0), 0, 1, False),
                              Entity((10, 10), 0, 1, False), Entity((0, 0), 0, 1, False)]\
               + [Mouse((random.randint(-20000, 20000), random.randint(-10000, 10000)),
                       random.randint(0, 360), 1, False) for _ in range(100)]
    units = []
    map_objects = []
    #seperating units and none units for performance
    for entity in entities:
        if isinstance(entity, Unit):
            units.append(entity)
        else:
            map_objects.append(entity)

    run = True
    while run:
        entities[0].rotation += 45*ui_data.delta_time
        ui_out = ui_tick(ui_data, entities)
        logic_tick(entities, units)
        run = ui_out.run


if __name__ == '__main__':
    main()