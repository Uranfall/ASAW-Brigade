from Entity import Entity


class Unit(Entity):
    def __init__(self, position: tuple[int, int], rotation: float):
        super().__init__(position, rotation)



