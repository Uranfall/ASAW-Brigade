from Entity import Entity
import Unit_AI


class Unit(Entity):
    STATIC_ROTATION = False
    
    def __init__(self, 
                 position: tuple[int, int], 
                 target_pos: tuple[int,int], 
                 rotation: float,
                 target_rotation: float,
                 speed: int,
                 selected: bool,
                 action_queue: list ):
        super().__init__(position, rotation)

    def move(self):
        ...
    def fire(self):
        ...
    def interact(self):
        ...
    def idle(self):
        ...
    
    

    
    
    




