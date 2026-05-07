from __future__ import annotations

from html import entities
from UnitClass import Unit
from Entity import Entity
from graphics.graphics_utility import Camera
from shared_utility import *
#navigation: UNIT -> NavNode -> find a path between them -> stop at closet NavNode from the click that isnt abstracted -> walk towards coordinates



#check if node is on entity
def check_walkable(node: Node, entities: list[Entity]):
    for entity in entities:
        if (entity.collision_points[0]<=node.x <= entity.collision_points[2] and
                entity.collision_points[1]<=node.y <= entity.collision_points[3] and
                entity.collision==True):
            return False
    return True


def point_in_rect(px, py, collision_points):
    return collision_points[0] <= px <= collision_points[2] and collision_points[1] <= py <= collision_points[3]


def ccw(ax, ay, bx, by, cx, cy):
    return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)


def segments_intersect(a1, a2, b1, b2):
    ax1, ay1 = a1
    ax2, ay2 = a2
    bx1, by1 = b1
    bx2, by2 = b2

    return (
        ccw(ax1, ay1, bx1, by1, bx2, by2) !=
        ccw(ax2, ay2, bx1, by1, bx2, by2)
    ) and (
        ccw(ax1, ay1, ax2, ay2, bx1, by1) !=
        ccw(ax1, ay1, ax2, ay2, bx2, by2)
    )


def line_intersects_rect(p1, p2, collision_points):
    # If either endpoint is inside the rectangle
    if point_in_rect(*p1, collision_points) or \
       point_in_rect(*p2, collision_points):
        return True

    # Rectangle corners
    top_left = (collision_points[0], collision_points[3])
    top_right = (collision_points[2], collision_points[3])
    bottom_left = (collision_points[0], collision_points[1])
    bottom_right = (collision_points[2], collision_points[1])

    # Rectangle edges
    edges = [
        (top_left, top_right),
        (top_right, bottom_right),
        (bottom_right, bottom_left),
        (bottom_left, top_left),
    ]

    # Check intersection with any edge
    for edge_start, edge_end in edges:
        if segments_intersect(p1, p2, edge_start, edge_end):
            return True

    return False

def path_clear(unitA: Unit, unitB: Unit, entities: list[Entity]):
        for entity in entities:
            positionA = unitA.position
            positionB = unitB.position
            scale = entity.IMAGE_SCALE
            img = entity.IMAGE
            collision_points = entity.get_collision_points()
            if line_intersects_rect(positionA, positionB, collision_points) and entity is not unitA or entity is not unitB:
                return False

        return True

