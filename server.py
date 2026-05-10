import random
import threading
import time

from Entities.Units import Mouse
from Entity import Entity
from GameData import GameDataServer
from UnitClass import Unit
from logic_main import logic_tick, LOGIC_DATA
from map import map_info
from shared_utility import get_closest_node


def server(game_data: GameDataServer):
    # entities = [Ground(), Unit((0, 0), 0, 1, False)]\
    map_objects, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE = map_info()

    units: list[Unit] = [Mouse((200, 200), 90, 1, 0), ] \
                        + [Mouse((random.randint(-2000, 2000), random.randint(-2000, 2000)),
                                 random.randint(0, 360), False, random.randint(0, 1)) for _ in range(10)]
    entities: list[Entity] = units + map_objects

    # Many of the variables above should be loaded into the server game data.

    for unit in units:
        unit.team = random.randint(0, 1)
        unit.current_node = get_closest_node(unit.get_position(), grid)
        unit.target_node = unit.current_node

    logic_data = LOGIC_DATA()
    player_team = 1

    run = True
    while run:
        logic_tick(entities, units, grid, logic_data, game_data)


def start_server(data):
    data.async_connect()
    while not data.is_connected():
        # print('still not')
        pass
    logic_data = LOGIC_DATA()
    while data.is_connected():
        logic_tick(data.get_entities(), data.get_units(), data.grid, logic_data, data)
        time.sleep(0.01)


if __name__ == '__main__':
    server_data = GameDataServer()
    t = threading.Thread(target=start_server, args=[server_data])
    t.start()
    input('press enter to disconnect...')
    print('disconnecting, this will take about 5 seconds...')
    server_data.disconnect()
    # print(data.get_error())

