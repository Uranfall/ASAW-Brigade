from html import entities

import pygame
from UnitClass import Unit
import heapq
from logic_utility import Node

#distance on a 2d grid
def manhattan_distance(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

#path finding logic
def a_star(start, goal, grid):
    open_list = []
    closed_list = set()

    heapq.heappush(open_list, (0, start))

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == goal:
            return reconstruct_path(current)

        closed_list.add(current)

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
                    heapq.heappush(open_list, (neighbor.f, neighbor))

    return None  # No path found


def get_neighbors(node, grid):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-directional
    neighbors = []

    for dx, dy in directions:
        x, y = node.x + dx, node.y + dy
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
            neighbors.append(grid[y][x])

    return neighbors


def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]