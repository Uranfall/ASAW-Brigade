import copy

from Entity import Entity
from Protocol.Command import Command
from UnitClass import Unit
from Node import Node
import threading


class GameData:
    def __init__(self):
        pass

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

    def get_commands(self) -> list[Command]:
        pass

    def connect(self):
        pass

    def async_connect(self) -> threading.Thread:
        t = threading.Thread(target=self.connect)
        return t


class GameDataLocal(GameData):
    def __init__(self, entities: list[Entity], units: list[Unit], grid: list[list[Node]], unit_spawn_points_team0: list[tuple[int,int]],
                 unit_spawn_points_team1: list[tuple[int,int]], grid_size):
        super().__init__()
        self.entities = entities
        self.units = units
        self.grid = grid
        self.unit_spawn_points_team0 = unit_spawn_points_team0
        self.unit_spawn_points_team1 = unit_spawn_points_team1
        self.grid_size = grid_size
        self.player0_currency = 2000
        self.player1_currency = 2000
        self.commands = []

    def get_layers(self):
        layers = []
        for entity in self.get_entities():
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

    def get_commands(self) -> list[Command]:
        return self.commands


class GameDataServer(GameData):
    pass


class GameDataClient(GameData):
    pass

