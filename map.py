from Entity import Entity
from logic_main import create_grid
from logic_utility import Node, check_walkable

#this is going to be the map with all the relavent information such as: entities (walls and stuff like that), grid, etc.
def map_info():
    map_entities: list[Entity] = [Entity((10, 10), 0, 1, False), Entity((0, 0), 0, 1, False)]
    unit_spawn_points_team0 = list[Node]
    unit_spawn_points_team1 = list[Node]

    WIDTH, HEIGHT = 800, 600
    GRID_SIZE = 20
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE
    #creates grid for the map
    grid = create_grid(GRID_WIDTH, GRID_HEIGHT)
    #if nodes are on entities or not
    for row in grid:
        for node in row:
           node.walkable = check_walkable(node, map_entities)

    return map_entities, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE