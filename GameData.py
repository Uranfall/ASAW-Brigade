import copy
import socket
from typing import Iterator

from Entity import Entity
from Protocol.Command import Command
from Protocol.Parameters import PORT
from UnitClass import Unit
from Node import Node
import threading

from VFX import VFX
from map import map_info


class GameData:
    def __init__(self):
        self.threads: list[threading.Thread] = []
        self.running = False  # Connect must stop as soon as it sees that self.running is false.

    def get_layers(self) -> list[list[Entity]]:
        """
        returns entities in layers, so they get rendered properly.
        """
        pass

    def get_entities(self) -> list[Entity]:
        pass

    def get_units(self) -> list[Unit]:
        pass

    def get_grid(self) -> list[list[Node]]:
        pass

    def add_command(self, command: Command):
        pass

    def get_commands(self) -> Iterator[Command]:
        pass

    def connect(self):
        pass

    def async_connect(self):
        self.disconnect()
        self.running = True
        self.threads = [threading.Thread(target=self.connect)]
        for thread in self.threads:
            thread.start()

    def disconnect(self):
        self.running = False
        for thread in self.threads:
            thread.join(timeout=5)

    def add_vfx(self, vfx: VFX):
        pass

    def clean_up_vfx(self):
        pass

    def is_connected(self) -> bool:
        pass

    def get_error(self) -> str | None:
        pass

    def get_currency(self):
        pass

    def get_player_currency(self, team: int) -> int:
        pass

    def update_player_currency(self, update: int, team: int):
        pass


class GameDataLocal(GameData):
    def __init__(self, entities: list[Entity], units: list[Unit], grid: list[list[Node]], unit_spawn_points_team0: list[tuple[int,int]],
                 unit_spawn_points_team1: list[tuple[int,int]], grid_size):
        super().__init__()
        self.entities = entities
        self.units = units
        self.grid = grid
        self.vfx = []
        self.unit_spawn_points_team0 = unit_spawn_points_team0
        self.unit_spawn_points_team1 = unit_spawn_points_team1
        self.grid_size = grid_size
        self.player0_currency = 2000
        self.player1_currency = 2000
        self.commands = []

    def get_layers(self):
        layers = []
        for entity in self.get_entities()+self.vfx:
            if len(layers) <= entity.RENDER_LAYER:
                layers += [[] for _ in range(entity.RENDER_LAYER-len(layers)+1)]
            layers[entity.RENDER_LAYER].append(entity)
        return layers

    def get_entities(self) -> list[Entity]:
        return self.entities.copy()

    def get_units(self) -> list[Unit]:
        return self.units.copy()

    def get_grid(self) -> list[list[Node]]:
        return copy.deepcopy(self.grid)


    def get_player_currency(self, team: int) -> int:
        if team == 0:
            return self.player0_currency
        elif team == 1:
            return self.player1_currency

    def update_player_currency(self, update: int, team: int):
        if team==0:
            self.player0_currency = self.player0_currency + update
        elif team==1:
            self.player1_currency = self.player1_currency + update


    def get_player_spawns(self, team: int) -> list[tuple[int,int]]:
        if team==0:
            return self.unit_spawn_points_team0
        elif team==1:
            return self.unit_spawn_points_team1
        return self.unit_spawn_points_team0

    def shift_player_spawns(self, team: int):
        if team==0:
            point0 = self.unit_spawn_points_team0[0]
            for x in range(1, len(self.unit_spawn_points_team0) - 1, 1):
                self.unit_spawn_points_team0[x-1] = self.unit_spawn_points_team0[x]
            self.unit_spawn_points_team0.append(point0)
        elif team==1:
            point0 = self.unit_spawn_points_team1[0]
            for x in range(1, len(self.unit_spawn_points_team1) - 1, 1):
                self.unit_spawn_points_team1[x - 1] = self.unit_spawn_points_team1[x]
            self.unit_spawn_points_team1.append(point0)

    def add_command(self, command: Command):
        self.commands.append(command)

    def get_commands(self) -> Iterator[Command]:
        while self.commands:
            yield self.commands.pop()

    def add_vfx(self, *vfx: VFX):
        self.vfx.extend(vfx)

    def clean_up_vfx(self):
        for vfx in self.vfx:
            if vfx.get_progress() > 1:
                self.vfx.remove(vfx)

    def get_unit_by_uid(self, uid: int):
        for unit in self.units:
            if unit.id == uid:
                return unit


class GameDataServer(GameData):
    def __init__(self):
        super().__init__()
        map_objects, grid, unit_spawn_points_team0, unit_spawn_points_team1, grid_size = map_info()
        self.entities = map_objects
        self.units = []
        self.grid = grid
        self.vfx = []
        self.unit_spawn_points_team0 = unit_spawn_points_team0
        self.unit_spawn_points_team1 = unit_spawn_points_team1
        self.grid_size = grid_size
        self.player0_currency = 2000
        self.player1_currency = 2000
        self.commands = []

        self.connected = 0
        self.error = None
        self.socket = socket.socket()
        self.socket.bind(('0.0.0.0', PORT))
        self.socket.listen()
        self.socket.settimeout(5)
        self.threads = []
        self.set_next_team = 0

    def connect(self):
        self.connected = False
        self.error = None
        try:
            client_socket, client_address = None, None
            while self.running:
                try:
                    (client_socket, client_address) = self.socket.accept()
                    break
                except socket.timeout:
                    pass
            team = self.set_next_team
            self.set_next_team = (self.set_next_team+1)%2
            self.connected += 1
            print('connected')
            while self.running and not self.is_connected():
                client_socket.send(str(self.connected).encode())
                client_socket.recv(1024)
            while self.running:
                data = client_socket.recv(1024).decode()
                self.commands.extend(map(Command.from_string, data[1:-1].split(',')))
                client_socket.send(self.get_message(team).encode())
                self.set_next_team = team

        except socket.error as e:
            print('error!', e)
            self.error = e
            self.connected -= 1

    def get_message(self, team: int):
        return '$'.join([''.join(map(str, self.entities+self.units)), self.get_player_currency(team)])

    def get_player_currency(self, team: int) -> int:
        if team == 0:
            return self.player0_currency
        elif team == 1:
            return self.player1_currency

    def async_connect(self):
        self.disconnect()
        self.running = True
        self.threads = [threading.Thread(target=self.connect), threading.Thread(target=self.connect)]
        for thread in self.threads:
            thread.start()

    def disconnect(self):
        super().disconnect()
        self.connected = 0

    def is_connected(self) -> bool:
        return self.connected >= 2

    def get_error(self):
        return self.error

    def get_unit_by_uid(self, uid: int):
        for unit in self.units:
            if unit.id == uid:
                return unit

    def get_commands(self) -> Iterator[Command]:
        while self.commands:
            yield self.commands.pop()


class GameDataClient(GameData):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.error = None

    def connect(self):
        self.connected = False
        self.error = None
        sock = socket.socket()
        sock.settimeout(5)
        try:
            sock.connect(("127.0.0.1", PORT))
            self.connected = True
            print('connected')

            while self.running:
                # print(sock.recv(1024))
                sock.send(b'hello!')

        except socket.error as e:
            print('error!', e)
            self.error = e
            self.running = False

    def disconnect(self):
        super().disconnect()
        self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def get_error(self):
        return self.error
