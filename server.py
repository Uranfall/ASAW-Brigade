import random
import threading
import time

from Entities.Units import Mouse
from Entity import Entity
from GameData import GameDataServer, GameDataClient
from UnitClass import Unit
from logic_main import logic_tick, LOGIC_DATA
from map import map_info
from shared_utility import get_closest_node

running = False


def start_server(data, single_game=False):
    while running:
        print('waiting for players')
        data.async_connect()
        while not data.is_connected() and running:
            pass
        print('new game started')
        logic_data = LOGIC_DATA()
        while data.connected and running:
            previous_update = time.time()
            logic_tick(data.get_entities(), data.get_units(), data.grid, logic_data, data)
            sleep_for = 1/60-(time.time()-previous_update)
            if sleep_for > 0:
                time.sleep(sleep_for)
        data.disconnect()
        data.__init__()
        print('game ended')
        if single_game:
            return


def host_game(ip: str):
    global running
    running = True
    tmp_server_data = GameDataServer()
    tmp_server_data.set_ip(ip)
    thread = threading.Thread(target=start_server, args=[tmp_server_data])
    thread.start()
    return tmp_server_data


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

