import random

import pygame

from Entity import Entity
from graphics_main import UIData, ui_tick


def main():
    ui_data = UIData(pygame.display.set_mode((500, 500), pygame.RESIZABLE))
    entities = [Entity((0, 0), 0)] + [Entity((random.randint(-20000, 20000), random.randint(-10000, 10000)),
                                             random.randint(0, 360)) for _ in range(2000)]
    run = True
    while run:
        ui_out = ui_tick(ui_data, entities)
        run = ui_out.run


if __name__ == '__main__':
    main()

