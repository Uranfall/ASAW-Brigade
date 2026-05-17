import copy
import math
from typing import Sequence, SupportsFloat
from Node import Node

def sign(num: float):
    return -1 if num < 1 else (1 if num > 0 else 0)


def angle_to_vector(angle: float, distance=1.0):
    """
    Input the angle in degrees.
    """
    # Added 90 degrees to the angle so it works the same as in pygame.
    return math.cos(math.radians(angle+90))*distance, math.sin(math.radians(angle+90))*distance

def get_closest_node(position: list,grid):
    min_distance = 9999
    closest_node = None
    for row in grid:
        for node in row:
            if node.walkable:
                if min_distance == 9999:
                    min_distance = math.dist([node.x,node.y], [position[0],position[1]])
                    closest_node = node
                if min_distance > math.dist([node.x,node.y], [position[0],position[1]]):
                    min_distance = math.dist([node.x,node.y], [position[0],position[1]])
                    closest_node = node
    return closest_node

def vector_to_angle(vector: list[float, float]):
    """
    Outputs the angle in degrees.
    """
    # Removed 90 degrees from the angle so it works the same as in pygame.
    return math.degrees(math.atan2(*vector[::-1]))-90


def rotate_vector(vector: list[float, float], angle):
    """
    Input the angle in degrees.
    """
    return angle_to_vector(vector_to_angle(vector)+angle, (vector[0]**2+vector[1]**2)**0.5)


def set_distance(vector: list[float, float],
                 pivot: list[float, float],
                 distance: float):
    new_direction = angle_to_vector(vector_to_angle([vector[0]-pivot[0], vector[1]-pivot[1]]), distance)
    return new_direction[0]+pivot[0], new_direction[1]+pivot[1]


def is_within_box(pos: list[float, float],
                  box: list[float, float, float, float]):
    return box[0] <= pos[0] <= box[2] and box[1] <= pos[1] <= box[3]

#note to self, fix this shit pls, this is absolute garbage code bro like wtf are you doing lock in
def boxes_overlap(box1: list[float, float, float, float],
                  box2: list[float, float, float, float]):
    return (is_within_box([box1[0],box1[1]] , box2) or is_within_box([box1[0],box1[3]] , box2) or
            is_within_box([box1[2],box1[1]] , box2) or is_within_box([box1[2],box1[3]] , box2))

def get_collision_points(pos:tuple[float, float],
                         dimensions          : tuple[float, float]):
    #width
    x1 = (pos[0] - dimensions[0] / 2)# left
    x2 = (pos[0] + dimensions[0] / 2)# right
    #height
    y1 = (pos[1] - dimensions[1] / 2)# bottom
    y2 = (pos[1] + dimensions[1] / 2)# top
    return [x1, y1, x2, y2]


def scale_box(box: list[int], scale: float):
    center_x = (box[0]+box[2])/2
    center_y = (box[1]+box[3])/2
    return [(box[0]-center_x)*scale+center_x, (box[1]-center_y)*scale+center_y,
            (box[2]-center_x)*scale+center_x, (box[3]-center_y)*scale+center_y]


LERP_CASES = {SupportsFloat: (lambda s, e, f, o: float(s) - (float(s) - float(e))*f),
              str: lambda s, e, f, o: s if f < 1 else e,
              Sequence: lambda s, e, f, o:
              s.__class__(map(lambda vals: lerp(vals[0], vals[1], f, overwrite_object=o),
                        zip(s, e))),
              bool: lambda s, e, f, o: s if f < 1 else e}


def lerp(start: any,
         end: any,
         factor: float,
         overwrite_object=False):

    # Sorry for the code looking so bad. I just wanted this function to work with most objects.
    # Just realized that the only line that does the lerping is not even in this function.

    if start is None or end is None:
        return LERP_CASES[bool](start, end, factor, overwrite_object)

    for t, func in LERP_CASES.items():
        if isinstance(start, t):
            return func(start, end, factor, overwrite_object)

    # If the object is something strange:
    if overwrite_object:
        out = start
    else:
        out = copy.deepcopy(start)
    out_dict = out if isinstance(out, dict) else out.__dict__
    end_dict = end if isinstance(end, dict) else end.__dict__
    for key, val in end_dict.items():
        out_dict[key] = lerp(out_dict[key], val, factor)
    return out


def stepped_interpolation(start,
                          end,
                          factor: float,
                          overwrite_object=False):
    if factor < 1:
        return lerp(start, end, 0, overwrite_object=overwrite_object)
    return lerp(start, end, 1, overwrite_object=overwrite_object)


class ValueCurve:
    def __init__(self, *points: tuple[any, float], extrapolate=False, interpolation=lerp):
        self.points = points
        self.extrapolate = extrapolate
        self.interpolation = interpolation

    def __call__(self, t: float):
        current_point = 0
        while current_point < len(self.points) - 2 and self.points[current_point+1][-1] < t:
            current_point += 1

        if not self.extrapolate and (self.points[current_point + 1][-1] <= t):
            return self.points[current_point + 1][0]
        if not self.extrapolate and self.points[current_point][-1] > t:
            return self.points[0][0]

        max_amount = self.points[current_point][-1] - self.points[current_point + 1][-1]
        current_amount = self.points[current_point][-1] - t
        if max_amount == 0:
            return self.points[current_point][0]
        return self.interpolation(self.points[current_point][0],
                                  self.points[current_point + 1][0],
                                  current_amount / max_amount)


def snap_to_grid(point: tuple[int, int], cell_size: int, keep_scale=False):
    return int(point[0] // cell_size) * (cell_size if keep_scale else 1),\
           int(point[1] // cell_size) * (cell_size if keep_scale else 1)

def shift_list_left(lst: list):
    for x in range(1,len(lst)-1,1):
        lst[x-1] = lst[x]
    return lst