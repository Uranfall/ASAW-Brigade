import math
import random
import time

import pygame

from Entity import Entity
from GlobalVariables import TEXT_RED_CURVE
from graphics.UI_Entities import Text, UIEntity, Button
from graphics.graphics_utility import Camera
from main import main
from shared_utility import ValueCurve


class Logo(Entity):
    IMAGE = pygame.image.load("Sprites/ui/new_highschool_herliya_logo.png")
    IMAGE_SCALE = 2


def main_menu():

    def play_button_action():
        nonlocal last_update
        main()
        last_update = time.time()

    play_button = Button((0, 0), (150, 50), Text((0, 0), 0, 'Play', TEXT_RED_CURVE), play_button_action)
    exit_button = Button((0, -60), (150, 50), Text((0, 0), 0, 'Exit', TEXT_RED_CURVE), exit)

    start_time = time.time()

    run = True
    camera = Camera([0, 1000], 1, pygame.display.set_mode((500, 500), pygame.RESIZABLE))

    menu_items: list[Entity] = [Logo((0, 1000), 0),
                                Text((0, 200),
                                     0,
                                     'ASAW',
                                     # (255, 100, 50),
                                     TEXT_RED_CURVE,
                                     100,
                                     time_offset=2),
                                play_button,
                                exit_button]

    screen_color_curve = ValueCurve(((240, 240, 240), 0.3),
                                    ((100, 100, 100), 0.7),
                                    ((70, 70, 70), 0.8),
                                    ((50, 70, 50), 1))

    camera_position_curve = ValueCurve(([0, 1000], 0), ([0, 925], 0.1), ([0, 50], 0.9), ([0, 0], 1))

    animation_start = 1
    animation_duration = 1

    last_update = time.time()

    while run:
        dt = time.time() - last_update
        last_update = time.time()

        animation_progress = (time.time()-start_time-animation_start)/animation_duration
        camera.position = camera_position_curve(animation_progress)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for button in menu_items:
                    if isinstance(button, Button):
                        if button.update_hover(camera):
                            if button.action is not None:
                                button.action()

        camera.tmp_offset = [math.sin(time.time()*0.7*2)*0.51, math.cos(time.time()*2)*0.51]

        for item in menu_items:
            item.draw(camera)
            if isinstance(item, UIEntity) and item.get_progress() > 1 and random.random() < 0.05*dt:
                item.creation_time = time.time()

        pygame.display.update()
        camera.screen.fill(screen_color_curve(animation_progress))


if __name__ == '__main__':
    main_menu()
