from Entity import Entity


class Unit(Entity):
    STATIC_ROTATION = False

    def __init__(self, position: tuple[int, int], rotation: float):
        super().__init__(position, rotation)



