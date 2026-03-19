
class Entity:
    def __init__(self, position: tuple[int, int], rotation: float, seeThrough):
        self.position = position
        self.rotation = rotation
        self.collision_points = []
        self.drawing_objects = []
        self.seeThrough = seeThrough




