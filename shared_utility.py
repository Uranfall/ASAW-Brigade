import math
from typing import Sequence, SupportsFloat
import pygame


def sign(num: float):
    return -1 if num < 1 else (1 if num > 0 else 0)


def angle_to_vector(angle: float, distance=1.0):
    return math.sin(math.radians(angle))*distance, math.cos(math.radians(angle))*distance


def vector_to_angle(vector: list[float, float]):
    return math.degrees(math.atan2(*vector[::-1]))


def is_within_box(pos: list[float, float] | tuple[float, float],
                  box: list[float, float, float, float] | tuple[float, float, float, float]):
    return box[0] <= pos[0] <= box[2] and box[1] <= pos[1] <= box[3]

def get_collision_points(pos:tuple[float, float] | tuple[int, int],
                         dimensions: tuple[float, float] | tuple[int, int]):
    x1 = (pos[0] - dimensions[0] / 2)
    x2 = (pos[0] + dimensions[0] / 2)
    y1 = (pos[1] - dimensions[0] / 2)
    y2 = (pos[1] + dimensions[0] / 2)
    return [x1, y1, x2, y2]

def lerp(start: float | Sequence[float], end: float | Sequence[float], factor: float):
    if isinstance(start, SupportsFloat):
        return float(start) - (float(start) - float(end))*factor
    return tuple(map(lambda vals: lerp(vals[0], vals[1], factor), zip(start, end)))


class ValueCurve:
    def __init__(self, *points: tuple[float | Sequence[float], float], extrapolate=False):
        self.points = points
        self.extrapolate = extrapolate

    def __call__(self, t: float):
        current_point = 0
        while current_point < len(self.points) - 2 and self.points[current_point+1][-1] < t:
            current_point += 1

        if not self.extrapolate and self.points[current_point + 1][-1] <= t:
            return self.points[current_point + 1][0]

        max_amount = self.points[current_point][-1] - self.points[current_point + 1][-1]
        current_amount = self.points[current_point][-1] - t
        if max_amount == 0:
            return self.points[current_point][0]
        return lerp(self.points[current_point][0], self.points[current_point + 1][0], current_amount / max_amount)


