from __future__ import annotations

from html import entities

from Entity import Entity
from graphics.graphics_utility import Camera
from shared_utility import *
#navigation: UNIT -> NavNode -> find a path between them -> stop at closet NavNode from the click that isnt abstracted -> walk towards coordinates



class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.g = 0  # Cost from start
        self.h = 0  # Heuristic cost
        self.parent = None
        self.f = 0  # Total cost


#check if node is on entity
def check_walkable(node: Node, entities: list[Entity]):
    for entity in entities:
        if (entity.collision_points[0]<=node.x <= entity.collision_points[2] and
                entity.collision_points[1]<=node.y <= entity.collision_points[3] and
                entity.collision==True):
            return False
    return True

def get_closest_node(position: list[float,float],grid) -> Node:
    min_distance = None
    closest_node = None
    for row in grid:
        for node in row:
            if min_distance is None:
                min_distance = abs(position[0] - node.x) + abs(position[1] - node.y)
                closest_node = node
            if min_distance > abs(position[0] - node.x) + abs(position[1] - node.y):
                min_distance = abs(position[0] - node.x) + abs(position[1] - node.y)
                closest_node = node
    return closest_node

#distance on a 2d grid


def path_clear(positionA: tuple(int,int), positionB: tuple(int,int), entities: list[Entity],camera: Camera):
        for entity in entities:
            scale = camera(entity.IMAGE_SCALE)
            img = entity.IMAGE
            collision_points = get_collision_points(entity.position, [img.get_width()*scale, img.get_height()*scale])
            #make a function and check if the y is the same
            if positionA[0] != positionB[0] and positionA[1] != positionB[1]:
                m = (positionA[1] - positionB[1]) / (positionA[0] - positionB[0])
                b = -1*m*positionA[0] + positionA[1]
                for x in range(collision_points[0],collision_points[2], 5):
                    if collision_points[1]<= m*x+b <= collision_points[3]:
                        return False
                return True
            #if X is the same
            elif positionA[0] != positionB[0]:
                if positionA[1] <= collision_points[1] <= positionB[1] or positionA[1] >= collision_points[1] >= positionB[1]:
                    return False
                return True
            #if Y is the same
            else:
                if positionA[0] <= collision_points[0] <= positionB[0] or positionA[0] >= collision_points[0] >= positionB[0]:
                    return False
                return True
        return True

