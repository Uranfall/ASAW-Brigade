from html import entities
import pygame
import heapq
from Node import Node

#distance on a 2d grid
def manhattan_distance(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

#path finding logic
def a_star(start, goal, grid):
    open_list = [] #nodes to explore
    closed_list = set() #explored nodes

    heapq.heappush(open_list, (0, start))

    while open_list:
        #get from the queue
        current = heapq.heappop(open_list)[1]
        #if we reached the goal
        if current == goal:
            return reconstruct_path(current)

        #send it to the list of checked nodes
        closed_list.add(current)
        #check all neighbouring nodes
        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_list or not neighbor.walkable:
                continue

            tentative_g = current.g + 1  # Cost to neighbor

            if neighbor not in open_list or tentative_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.h = manhattan_distance(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_list:
                    #add to open list
                    heapq.heappush(open_list, (neighbor.f, neighbor))

    return None  # No path found

#get neighbouring nodes from all 4 directions
def get_neighbors(node, grid):
    directions = [(0, 50), (50, 0), (0, -50), (-50, 0)]  # 4-directional
    neighbors = []

    for dx, dy in directions:
        x, y = node.x + dx, node.y + dy
        if -1*len(grid[0])/2 <= x < len(grid[0])/2 and -1*len(grid)/2 <= y < len(grid)/2:
            neighbors.append(grid[y][x])

    return neighbors


def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    print(path[::-1])
    return path[::-1]