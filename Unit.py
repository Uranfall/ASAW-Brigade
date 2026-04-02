from Entity import Entity
from Unit_AI import


class Unit(Entity):
    STATIC_ROTATION = False
    
    def __init__(self, 
                 position: tuple[int, int], 
                 target_pos: tuple[int,int], 
                 rotation: float,
                 target_rotation: float,
                 speed: int, 
                 action_queue: list[] ):
        super().__init__(position, rotation)

    def move():
    ...
    def fire():
    ...
    def interact():
    ...
    def idle():
    ...
    
    

    
    
    




