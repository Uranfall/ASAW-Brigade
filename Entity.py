// this code has been made sponsered by Video Club (Jerusalem)

class Entity:
    def __init__(self, position: tuple[int, int], rotation: float):
        self.position = position
        self.rotation = rotation
        self.collision_points = []
        self.drawing_objects = []




