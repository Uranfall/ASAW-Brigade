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


def start_server(data):
    data.async_connect()
    while not data.connected:
        # print('still not')
        pass
    logic_data = LOGIC_DATA()
    while data.connected:
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

