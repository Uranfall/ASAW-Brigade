import pygame

from Entity import Entity
from graphics_main import UIData, ui_tick


def main():
    ui_data = UIData(pygame.display.set_mode((500, 500), pygame.RESIZABLE))
    entities = [Entity((0, 0), 0)]
    run = True
    while run:
        ui_out = ui_tick(ui_data, entities)
        run = ui_out.run


if __name__ == '__main__':
    main()

