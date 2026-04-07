import random

import pygame

from VFX import Explosion
from graphics.Debug_Entities import DebugRay, DebugLine
from UnitClass import Unit
from Entity import Entity
from graphics.Ground import Ground
from graphics.graphics_main import UIData, ui_tick
from logic_main import logic_tick


def main():
    ui_data = UIData(pygame.display.set_mode((500, 500), pygame.RESIZABLE))
    player_team = 0
    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    entities = [Unit((0, 0), 0, 1, False)]\
               + [Unit((random.randint(-20000, 20000), random.randint(-10000, 10000)),
                       random.randint(0, 360), 1, False) for _ in range(500)]
    units = []
    for entity in entities:
        if type(entity) is Unit:
            units.append(entity)

    run = True
    while run:
        entities[0].rotation += 45*ui_data.delta_time
        ui_out = ui_tick(ui_data, entities)
        logic_tick(entities, units)
        run = ui_out.run


if __name__ == '__main__':
    main()