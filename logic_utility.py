from __future__ import annotations

from html import entities

from Entity import Entity
from graphics.graphics_utility import Camera
from shared_utility import *
#navigation: UNIT -> NavNode -> find a path between them -> stop at closet NavNode from the click that isnt abstracted -> walk towards coordinates


def shift_list_left(lst: list):
    for x in range(1,len(lst)-1,1):
        lst[x-1] = lst[x]
    return lst

#check if node is on entity
def check_walkable(node: Node, entities: list[Entity]):
    for entity in entities:
        if (entity.collision_points[0]<=node.x <= entity.collision_points[2] and
                entity.collision_points[1]<=node.y <= entity.collision_points[3] and
                entity.collision==True):
            return False
    return True


#distance on a 2d grid


def path_clear(positionA: tuple(int,int), positionB: tuple(int,int), entities: list[Entity]):
        for entity in entities:
            scale = entity.IMAGE_SCALE
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

