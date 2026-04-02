import math


def sign(num: float):
    return -1 if num < 1 else (1 if num > 0 else 0


def angle_to_vector(angle: float, distance=1.0):
    return math.sin(math.radians(angle))*distance, math.cos(math.radians(angle))*distance


def vector_to_angle(vector: list[float, float]):
    return math.degrees(math.atan2(*vector[::-1]))

