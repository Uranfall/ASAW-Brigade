from __future__ import annotations  # So we can reference the class in itself.


class Entity:
    #seeThrough - Boolean that checks if you can see through the entity or not, used for ray logic
    #collision - if a unit can go through the object or not
    def __init__(self,
                 position: tuple[int, int],
                 rotation: float,
                 see_through=False,
                 collision=True):
        self.position = position
        self.rotation = rotation
        self.collision_points = []
        self.drawing_objects = []
        self.see_through = see_through
        self.collision = collision

    def is_colliding_with(self, entity: Entity) -> bool:
        ...

    def does_ray_intersect(self, ray_position, ray_rotation: float) -> bool:
        ...

    def game_tick(self, game_state):  # Will only be implemented for moving objects like units and bullets.
        pass
