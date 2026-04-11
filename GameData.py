import copy

from Entity import Entity
from UnitClass import Unit
from logic_utility import Node
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

    def connect(self):
        pass

    def async_connect(self) -> threading.Thread:
        t = threading.Thread(target=self.connect)
        return t


class GameDataLocal(GameData):
    def __init__(self, entities: list[Entity], units: list[Unit], grid: list[list[Node]], unit_spawn_points_team0,
                 unit_spawn_points_team1, grid_size):
        super().__init__()
        self.entities = entities
        self.units = units
        self.grid = grid
        self.unit_spawn_points_team0 = unit_spawn_points_team0
        self.unit_spawn_points_team1 = unit_spawn_points_team1
        self.grid_size = grid_size

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


class GameDataServer(GameData):
    pass


class GameDataClient(GameData):
    pass

