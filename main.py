import random

import pygame

from graphics.Debug_Entities import DebugRay
from UnitClass import Unit
from Entity import Entity
from graphics.Ground import Ground
from graphics.graphics_main import UIData, ui_tick


def main():
    ui_data = UIData(pygame.display.set_mode((500, 500), pygame.RESIZABLE))
    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    entities = [Unit((0, 0), 0, 1, False)]\
               + [Unit((random.randint(-20000, 20000), random.randint(-10000, 10000)),
                       random.randint(0, 360), 1, False) for _ in range(500)]
    units_Selected = []
    run = True
    while run:
        entities[0].rotation += 45*ui_data.delta_time
        ui_out, units_Selected = ui_tick(ui_data, entities, units_Selected)
        for unit in units_Selected:
            unit.set_position( (unit.get_position()[0] + 4, unit.get_position()[1]) )
        run = ui_out.run


if __name__ == '__main__':
    main()