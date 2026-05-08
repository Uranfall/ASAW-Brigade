import pygame

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
            spawn_points = game_data.get_player_spawns(player_team)
            money = game_data.get_player_currency(player_team)
            if money >= 250:
                game_data.update_player_currency(-500, player_team)
                newUnit = Mouse(spawn_points[0], 90, False, player_team)
                newUnit.current_node = get_closest_node(newUnit.get_position(), game_data.get_grid())
                newUnit.target_node = newUnit.current_node
                # add unit
                units.append(newUnit)
                entities.append(newUnit)
                # shift list left, set the next spawn as the one the next unit is going to use
                game_data.shift_player_spawns(player_team)

        def create_soldier():
            spawn_points = game_data.get_player_spawns(player_team)
            money = game_data.get_player_currency(player_team)
            if money >= 500:
                game_data.update_player_currency(-500, player_team)
                newUnit = Soldier(spawn_points[0], 90, False, player_team)
                newUnit.current_node = get_closest_node(newUnit.get_position(), game_data.get_grid())
                newUnit.target_node = newUnit.current_node
                # add unit
                units.append(newUnit)
                entities.append(newUnit)
                # shift list left, set the next spawn as the one the next unit is going to use
                game_data.shift_player_spawns(player_team)

        def create_tank():
            spawn_points = game_data.get_player_spawns(player_team)
            money = game_data.get_player_currency(player_team)
            if money >= 1000:
                game_data.update_player_currency(-500, player_team)
                newUnit = Tank(spawn_points[0], 90, False, player_team)
                newUnit.current_node = get_closest_node(newUnit.get_position(), game_data.get_grid())
                newUnit.target_node = newUnit.current_node
                # add unit
                units.append(newUnit)
                entities.append(newUnit)
                # shift list left, set the next spawn as the one the next unit is going to use
                game_data.shift_player_spawns(player_team)

        player_team = 1

        # UI related code
        ui_data = UIData(screen)
        exit_button = Button((0, 220), (100, 40), Text((0, 0), 0, 'Quit', TEXT_RED_CURVE), action=quit_main)
        player_currency = Text((120, 220), 0, str(game_data.get_player_currency(player_team)) + "$", TEXT_RED_CURVE)
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
            player_currency.text = str(game_data.get_player_currency(player_team)) + "$"
            run = run and ui_out.run


if __name__ == '__main__':
    data = GameDataClient()
    data.async_connect()
    while not data.connected:
        # print('still not')
        pass
    print(data.get_error())

