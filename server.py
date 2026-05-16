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
    while running:
        print('waiting for players')
        data.async_connect()
        while not data.is_connected():
            pass
        print('new game started')
        logic_data = LOGIC_DATA()
        while data.connected:
            previous_update = time.time()
            logic_tick(data.get_entities(), data.get_units(), data.grid, logic_data, data)
            sleep_for = 1/60-(time.time()-previous_update)
            if sleep_for > 0:
                time.sleep(sleep_for)
        data.disconnect()
        data.__init__()
        print('game ended')


if __name__ == '__main__':
    running = True
    server_data = GameDataServer()
    t = threading.Thread(target=start_server, args=[server_data])
    t.start()
    input('press enter to disconnect...')
    print('disconnecting, this might take about 5 seconds...')
    running = False
    server_data.disconnect()
    # print(data.get_error())

