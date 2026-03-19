
class Entity:
    #seeThrough - Boolean that checks if you can see through the entity or not, used for ray logic
    #collision - if a unit can go through the object or not
    def __init__(self, position: tuple[int, int], rotation: float, seeThrough, collision):
        self.position = position
        self.rotation = rotation
        self.collision_points = []
        self.drawing_objects = []
        self.seeThrough = seeThrough
        self.collision = collision




