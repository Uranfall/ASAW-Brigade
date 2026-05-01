import math
import random
import time

import pygame
import screeninfo

from Entity import Entity
from GlobalVariables import TEXT_RED_CURVE
from graphics.UI_Entities import Text, UIEntity, Button, TextBox, RotatingGear1, RotatingGear2
from graphics.graphics_utility import Camera, CinematicCamera
from main import main
from shared_utility import ValueCurve, stepped_interpolation
from screeninfo import get_monitors


class Logo(Entity):
    IMAGE = pygame.image.load("Sprites/ui/new_highschool_herliya_logo.png")
    IMAGE_SCALE = 2


def main_menu():
    screen_color_curve: ValueCurve | None = None
    camera_position_curve: ValueCurve | None = None
    animation_start: float | None = None
    animation_duration: float | None = None

    def start_camera_animation():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve(((240, 240, 240), 0.3),
                                        ((100, 100, 100), 0.4),
                                        ((70, 70, 70), 0.5),
                                        ((50, 70, 50), 0.7))
        camera_position_curve = ValueCurve(([0, 1000], 0), ([0, 1020], 0.15), ([0, -10], 0.3), ([0, 0], 0.8),
                                           interpolation=stepped_interpolation)
        animation_start = 1
        animation_duration = 1
        start_time = time.time()

    def return_to_start():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.25),
                                        ((50, 70, 50), 0.75))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([0, 0], 0.2))
        animation_duration = 1
        start_time = time.time()

    def start_local():
        nonlocal last_update
        main()
        last_update = time.time()

    def play_button_action():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.25), ((50, 50, 50), 0.75))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([1000, 0], 0.2))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()

    def online_menu():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.25), ((50, 50, 60), 0.75))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([2000, 0], 0.2))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()

    def online_loading_screen():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.1), ((120, 120, 160), 0.3))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([2000, 2000], 0.35))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()

    def settings():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.1), ((55, 55, 55), 0.3))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([-1000, 0], 0.35))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()

    def set_to_full_screen():
        camera.screen = pygame.display.set_mode((screeninfo.get_monitors()[0].x, screeninfo.get_monitors()[0].y))
        pygame.display.toggle_fullscreen()
        toggle_full.action = reset_display
        toggle_full.text.text = 'To Windowed'

    def reset_display():
        pygame.display.toggle_fullscreen()
        camera.screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        toggle_full.action = set_to_full_screen
        toggle_full.text.text = 'To Fullscreen'

    play_local = Button((1000, 40), (150, 50), Text((0, 0), 0, 'Local', TEXT_RED_CURVE), start_local)
    play_online = Button((1000, -20), (150, 50), Text((0, 0), 0, 'Online', TEXT_RED_CURVE), online_menu)
    online_start = Button((2000, -20), (150, 50), Text((0, 0), 0, 'Start', TEXT_RED_CURVE), online_loading_screen)
    back_to_online_menu = Button((2000, 1820), (150, 50), Text((0, 0), 0, 'Cancel', (255, 255, 255)), online_menu,
                                 color=ValueCurve(((120, 120, 160), 0), ((125, 125, 170), 1)),
                                 border_color=(120, 120, 160))
    back_to_start = Button((1000, -80), (150, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), return_to_start)
    back_to_start2 = Button((-1000, -200), (150, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), return_to_start)
    toggle_full = Button((-1000, -140), (270, 50), Text((0, 0), 0, 'To Fullscreen', TEXT_RED_CURVE), set_to_full_screen)
    back_to_play = Button((2000, -80), (150, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), play_button_action)
    play_button = Button((0, 0), (150, 50), Text((0, 0), 0, 'Play', TEXT_RED_CURVE), play_button_action)
    settings_button = Button((0, -60), (150, 50), Text((0, 0), 0, 'Settings', TEXT_RED_CURVE), settings)
    exit_button = Button((0, -120), (150, 50), Text((0, 0), 0, 'Exit', TEXT_RED_CURVE), exit)

    start_time = time.time()

    run = True
    camera = CinematicCamera([0, 1000], 1, pygame.display.set_mode((500, 500), pygame.RESIZABLE))

    menu_items: list[Entity] = [Logo((0, 1000), 0),
                                Text((0, 190),
                                     0,
                                     'ASAW',
                                     # (255, 100, 50),
                                     TEXT_RED_CURVE,
                                     100,
                                     time_offset=2,
                                     font_name='Stencil',
                                     # font_name='OCR A Extended',
                                     bold=False, italic=False),
                                play_local,
                                play_online,
                                online_start,
                                back_to_online_menu,
                                Text((2000, 2000), 0, "Connecting to server...",
                                     (255, 255, 255)),
                                Text((2000, 1960), 0, "The game will start in a minute, trust me!",
                                     (255, 255, 255),
                                     20),
                                back_to_start,
                                back_to_start2,
                                toggle_full,
                                back_to_play,
                                # Text((1900, 45), 0, 'Username:', TEXT_RED_CURVE),
                                TextBox((2000, 60), (200, 50), 10, default_text='Your Name'),
                                play_button,
                                settings_button,
                                exit_button,
                                RotatingGear1((-1250, 200), 0, 360/10),
                                RotatingGear2((-1500, 100), 30, -360/10),
                                RotatingGear2((-980, 275), 10, -360/10),
                                ]

    start_camera_animation()

    last_update = time.time()

    while run:
        dt = time.time() - last_update
        last_update = time.time()

        animation_progress = (time.time()-start_time-animation_start)/animation_duration
        camera.target_position = camera_position_curve(animation_progress)
        camera.animate(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for item in menu_items:
                    if isinstance(item, TextBox):
                        item.selected = False
                    if isinstance(item, Button):
                        if item.update_hover(camera):
                            if item.action is not None:
                                item.action()
                animation_progress = (time.time() - start_time - animation_start) / animation_duration
                camera.target_position = camera_position_curve(animation_progress)
            if event.type == pygame.KEYUP:
                for item in menu_items:
                    if isinstance(item, TextBox):
                        item.key_down(event.unicode)

        camera.tmp_offset = [math.sin(time.time()*0.7*2)*0.51, math.cos(time.time()*2)*0.51]

        for item in menu_items:
            item.draw(camera)
            if isinstance(item, UIEntity) and item.TRIGGERABLE and\
                    item.get_progress() > 1 and random.random() < 0.05*dt:
                item.creation_time = time.time()

        pygame.display.update()
        camera.screen.fill(screen_color_curve(animation_progress))


if __name__ == '__main__':
    main_menu()
