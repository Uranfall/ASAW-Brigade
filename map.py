from Entity import Entity
from graphics.Ground import Ground
from logic_main import create_grid
from Node import Node
from logic_utility import check_walkable

#this is going to be the map with all the relavent information such as: entities (walls and stuff like that), grid, etc.
def map_info():
    map_entities: list[Entity] = [Entity((10, 10), 0, 1, False), Entity((0, 0), 0, 1, False)]
    unit_spawn_points_team0 = [[-500, -500], [0, -500], [500, -500]]
    unit_spawn_points_team1 = [[-500, 500], [0, 500], [500, 500]]
    GRID_SIZE = 10
    WIDTH_START, WIDTH_END = -20000//GRID_SIZE, 20000//GRID_SIZE
    HEIGHT_START, HEIGHT_END = -20000//GRID_SIZE, 20000//GRID_SIZE

    #creates grid for the map
    grid = create_grid(WIDTH_START, WIDTH_END, HEIGHT_START, HEIGHT_END)
    #if nodes are on entities or not
    for row in grid:
        for node in row:
            node.walkable = check_walkable(node, map_entities)

    map_entities.append(Ground())

    return map_entities, grid, unit_spawn_points_team0, unit_spawn_points_team1, GRID_SIZE