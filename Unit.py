from Entity import Entity
import Unit_AI


class Unit(Entity):
    STATIC_ROTATION = False
    
    def __init__(self,
                 unit_type: str,
                 position: tuple[int, int], 
                 target_pos: tuple[int,int],
                 rotation: float,
                 target_rotation: float,
                 speed: int,
                 selected: bool,
                 action_list: list):
        super().__init__(position, rotation, selected)
        self.action_list = action_list
        self.target_pos = target_pos
        self.target_rotation = target_rotation
        self.speed = speed
        self.unit_type = unit_type


    def move(self):
        ...
    def fire(self):
        ...
    def interact(self):
        ...
    def idle(self):
        ...
    
    

    
    
    




