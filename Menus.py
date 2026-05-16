import math
import random
import time

import pygame
import screeninfo

import threading
from server import host_server
import client
from Entities.Bonus import CatGunner, HandGun
from Entity import Entity
from GameData import GameDataLocal, GameDataClient
from GlobalVariables import TEXT_RED_CURVE
from VFX import GunFire, SmokeTrail
from graphics.Ground import Ground
import graphics.Ground as GroundProperties
from graphics.UI_Entities import Text, UIEntity, Button, TextBox, RotatingGear1, RotatingGear2
from graphics.graphics_main import UIData, ui_tick
from graphics.graphics_utility import Camera, CinematicCamera
from main import main
from shared_utility import ValueCurve, stepped_interpolation


class Logo(Entity):
    IMAGE = pygame.image.load("Sprites/ui/new_highschool_herliya_logo.png")
    IMAGE_SCALE = 2


def gun_range(screen=pygame.display.set_mode((500, 500), pygame.RESIZABLE)):
    def quit_gun_range():
        nonlocal run
        run = False

    def bang_bang():
        ui_data.ui_entities.append(GunFire((-70, 175), 0))

    def pew_pew():
        ui_data.ui_entities.append(SmokeTrail((-30, -135), 90, distance=1000))

    ground = Ground()

    ui_data = UIData(screen)
    exit_button = Button((0, -200), (100, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), action=quit_gun_range)
    exit_button.creation_time = 0

    ui_data.add_on_screen_entity(exit_button)

    game_data = GameDataLocal([ground,
                               CatGunner((0, 150), 0),
                               Button((200, 150), (190, 50), Text((0, 0), 0, 'Bang Bang!', TEXT_RED_CURVE),
                                      action=bang_bang),
                               Button((200, -150), (175, 50), Text((0, 0), 0, 'Pew Pew!', TEXT_RED_CURVE),
                                      action=pew_pew),
                               HandGun((0, -150), 0)], [], [], None, None, 10)

    run = True
    while run:

        out = ui_tick(ui_data, game_data)

        if not out.run:
            exit()


def ground_properties(screen=pygame.display.set_mode((500, 500), pygame.RESIZABLE)):
    def quit_ground_properties():
        nonlocal run
        run = False

    ground = Ground()

    ui_data = UIData(screen)
    exit_button = Button((0, -200), (100, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), action=quit_ground_properties)
    exit_button.creation_time = 0

    tile_distance = TextBox((-120, 200),
                            (225, 50),
                            max_length=6,
                            default_text='Resolution')
    tile_distance.creation_time = 0

    quality = TextBox((-120, 140),
                      (220, 50),
                      max_length=6,
                      default_text='Quality')

    quality.creation_time = 0

    ui_data.add_on_screen_entity(exit_button)
    ui_data.add_on_screen_entity(tile_distance)
    ui_data.add_on_screen_entity(quality)

    game_data = GameDataLocal([Logo((0, 0), 0), ground], [], [], None, None, 10)

    run = True
    while run:
        update_ground = False
        if tile_distance.text.text.isnumeric():
            tmp = int(tile_distance.text.text)
            if tmp != 0 and tmp != GroundProperties.tile_distance:
                GroundProperties.tile_distance = tmp
                update_ground = True
        else:
            tmp = 800
            if tmp != GroundProperties.tile_distance:
                GroundProperties.tile_distance = tmp
                update_ground = True

        if quality.text.text.isnumeric():
            tmp = int(quality.text.text)
            if tmp != 0 and tmp != GroundProperties.quality:
                GroundProperties.quality = tmp
                update_ground = True
        else:
            tmp = 200
            if tmp != GroundProperties.quality:
                GroundProperties.quality = tmp
                update_ground = True

        if update_ground:
            ground.tiles = dict()

        out = ui_tick(ui_data, game_data)

        if not out.run:
            exit()


def main_menu():

    game_data: GameDataClient | None = None
    trying_to_connect = False

    last_time_pressed_enter = 0
    enter_text = Text((-1000, -3035), 0, 'Not the key you dummy!', TEXT_RED_CURVE)

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

    def reset_animation():
        nonlocal animation_progress
        animation_progress = (time.time() - start_time - animation_start) / animation_duration
        camera.target_position = camera_position_curve(animation_progress)

    def return_to_start():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.25),
                                        ((50, 70, 50), 0.75))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([0, 0], 0.2))
        animation_duration = 1
        start_time = time.time()
        reset_animation()

    def start_local():
        nonlocal last_update
        main()
        last_update = time.time()
        reset_animation()

    def play_button_action():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.25), ((50, 50, 50), 0.75))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([1000, 0], 0.2))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()
        reset_animation()

    def online_menu():
        nonlocal screen_color_curve,\
            camera_position_curve, \
            animation_start,\
            animation_duration,\
            start_time,\
            trying_to_connect
        trying_to_connect = False
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.25), ((50, 50, 60), 0.75))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([2000, 0], 0.2))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()
        reset_animation()

    def host_game():
        host_server(IP, game_data)
        online_loading_screen()
    def online_loading_screen():
        nonlocal screen_color_curve, \
            camera_position_curve, \
            animation_start, \
            animation_duration, \
            start_time, \
            game_data, \
            trying_to_connect
        trying_to_connect = True
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.1), ((120, 120, 160), 0.3))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([2000, 2000], 0.35))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()
        reset_animation()

        if game_data is not None:
            game_data.disconnect()
        game_data = GameDataClient()
        game_data.async_connect()

    def settings():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.1), ((55, 55, 55), 0.3))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([-1000, 0], 0.35))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()
        reset_animation()

    def set_to_full_screen():
        camera.screen = pygame.display.set_mode((screeninfo.get_monitors()[0].width,
                                                 screeninfo.get_monitors()[0].height))
        pygame.display.toggle_fullscreen()
        toggle_full.action = reset_display
        toggle_full.text.text = 'To Windowed'

    def reset_display():
        pygame.display.toggle_fullscreen()
        camera.screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        toggle_full.action = set_to_full_screen
        toggle_full.text.text = 'To Fullscreen'

    def gun_range_dungeon():
        nonlocal screen_color_curve, camera_position_curve, animation_start, animation_duration, start_time
        screen_color_curve = ValueCurve((screen_color_curve(animation_progress), 0.1), ((40, 40, 40), 0.8))
        camera_position_curve = ValueCurve((camera.target_position, 0), ([-1000, -3000], 0.35))
        animation_start = 0
        animation_duration = 1
        start_time = time.time()
        reset_animation()

    play_local = Button((1000, 40), (150, 50), Text((0, 0), 0, 'Local', TEXT_RED_CURVE), start_local)
    play_online = Button((1000, -20), (150, 50), Text((0, 0), 0, 'Online', TEXT_RED_CURVE), online_menu)
    online_start = Button((2000, -20), (150, 50), Text((0, 0), 0, 'Start', TEXT_RED_CURVE), online_loading_screen)
    online_host = Button((2000, -80), (150, 50), Text((0, 0), 0, 'Host', TEXT_RED_CURVE), host_game)
    back_to_online_menu = Button((2000, 1820), (150, 50), Text((0, 0), 0, 'Cancel', (255, 255, 255)), online_menu,
                                 color=ValueCurve(((120, 120, 160), 0), ((125, 125, 170), 1)),
                                 border_color=(120, 120, 160))
    back_to_start = Button((1000, -80), (150, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), return_to_start)
    back_to_start2 = Button((-1000, -200), (150, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), return_to_start)
    toggle_full = Button((-1000, -80), (270, 50), Text((0, 0), 0, 'To Fullscreen', TEXT_RED_CURVE), set_to_full_screen)
    back_to_play = Button((2000, -140), (150, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE), play_button_action)
    play_button = Button((0, 0), (150, 50), Text((0, 0), 0, 'Play', TEXT_RED_CURVE), play_button_action)
    settings_button = Button((0, -60), (150, 50), Text((0, 0), 0, 'Settings', TEXT_RED_CURVE, size=28), settings)
    settings_button2 = Button((-1000, -3150), (100, 50), Text((0, 0), 0, 'Back', TEXT_RED_CURVE, size=28), settings)
    gun_range_button = Button((-1000, -20), (200, 50), Text((0, 0), 0, 'Gun Range', TEXT_RED_CURVE), gun_range_dungeon)
    gun_range_enter = Button((-1000, -3000), (200, 50), Text((0, 0), 0, 'Enter', TEXT_RED_CURVE), gun_range)
    ground_settings = Button((-1000, -80), (320, 50), Text((0, 0), 0, 'Ground Properties', TEXT_RED_CURVE),
                             ground_properties)
    exit_button = Button((0, -120), (150, 50), Text((0, 0), 0, 'Exit', TEXT_RED_CURVE), exit)

    start_time = time.time()

    run = True
    camera = CinematicCamera([0, 1000], 1, pygame.display.set_mode((500, 500), pygame.RESIZABLE))

    menu_items: list[Entity] = [Logo((0, 1000), 0),
                                RotatingGear1((-1250, 200), 0, 360 / 10),
                                RotatingGear2((-1500, 100), 30, -360 / 10),
                                RotatingGear2((-980, 275), 10, -360 / 10),
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
                                online_host,
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
                                TextBox((2000, 60), (200, 50), 10, default_text='Server IP'),
                                play_button,
                                settings_button,
                                ground_settings,
                                gun_range_button,
                                settings_button2,
                                gun_range_enter,
                                exit_button,
                                ]

    start_camera_animation()
    IP = "0.0.0.0"
    last_update = time.time()

    while run:
        if game_data is not None and game_data.is_connected() and game_data.start_time != 0:
            client.start(game_data, camera.screen)
            game_data.set_ip(IP)
            game_data.disconnect()
            online_menu()
        if trying_to_connect and game_data is not None and game_data.get_error() is not None:
            game_data.async_connect()

        dt = time.time() - last_update
        last_update = time.time()

        animation_progress = (time.time() - start_time - animation_start) / animation_duration
        camera.target_position = camera_position_curve(animation_progress)
        camera.animate(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                for item in menu_items:
                    if isinstance(item, TextBox):
                        item.pressed_key(event.unicode)
                        IP = item.text.text
                if event.key == pygame.K_RETURN:
                    last_time_pressed_enter = time.time()
                    enter_text.creation_time = time.time()
        if time.time() - last_time_pressed_enter < 5:
            enter_text.draw(camera)

        camera.tmp_offset = [math.sin(time.time() * 0.7 * 2) * 0.51, math.cos(time.time() * 2) * 0.51]

        for item in menu_items:
            item.draw(camera)
            if isinstance(item, UIEntity) and item.TRIGGERABLE and \
                    (item.get_progress() > 1 or item.LIFETIME == math.inf) and random.random() < 0.025 * dt:
                item.creation_time = time.time()

        pygame.display.update()
        camera.screen.fill(screen_color_curve(animation_progress))


if __name__ == '__main__':
    main_menu()
