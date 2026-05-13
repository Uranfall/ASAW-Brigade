import pygame

from Protocol.Command import Command
from Entities.Units import Mouse, Soldier, Tank
from GameData import GameDataClient
from GlobalVariables import TEXT_RED_CURVE
from graphics.UI_Entities import Text, Button
from graphics.graphics_main import ui_tick, UIData
from shared_utility import get_closest_node


def start(game_data: GameDataClient, screen: pygame.display):

        def quit_main():
            nonlocal run
            run = False

        def create_mouse():
            game_data.add_command(Command("spawn",Mouse.NAME).__str__())

        def create_soldier():
            game_data.add_command(Command("spawn",Soldier.NAME).__str__())

        def create_tank():
            game_data.add_command(Command("spawn",Tank.NAME).__str__())


        # UI related code
        ui_data = UIData(screen)
        exit_button = Button((0, 220), (100, 40), Text((0, 0), 0, 'Quit', TEXT_RED_CURVE), action=quit_main)
        player_currency = Text((120, 220), 0, str(game_data.currency) + "$", TEXT_RED_CURVE)
        exit_button.creation_time = 0
        ui_data.add_on_screen_entity(exit_button)
        c_b1 = Button((-130, -220), (100, 40), Text((0, 0), 0, 'Mouse', TEXT_RED_CURVE, size=30), action=create_mouse)
        c_b2 = Button((0, -220), (140, 40), Text((0, 0), 0, 'Soldier', TEXT_RED_CURVE, size=30), action=create_soldier)
        c_b3 = Button((130, -220), (100, 40), Text((0, 0), 0, 'Tank', TEXT_RED_CURVE, size=30),
                      action=create_tank)
        ui_data.add_on_screen_entity(c_b1)
        ui_data.add_on_screen_entity(c_b2)
        ui_data.add_on_screen_entity(c_b3)
        ui_data.add_on_screen_entity(Text((0, -180), 0, 'Creation Menu:', TEXT_RED_CURVE))
        ui_data.add_on_screen_entity(player_currency)

        run = True
        while run:
            ui_out = ui_tick(ui_data, game_data)
            player_currency.text = str(game_data.currency) + "$"
            run = run and ui_out.run


if __name__ == '__main__':
    data = GameDataClient()
    data.async_connect()
    while not data.connected:
        print('still not')

    print(data.get_error())

