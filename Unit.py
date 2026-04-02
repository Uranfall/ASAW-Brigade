import math
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
                 act_list: list):
        super().__init__(position, rotation, selected)
        self.act_list = act_list
        self.target_pos = position
        self.target_rotation = rotation
        self.unit_type = unit_type

    def draw(self, camera: Camera):
        super(Unit, self).draw(camera)
        if self.selected:
            pygame.draw.circle(camera.screen,
                               (255, 0, 0),
                               camera(*self.position),
                               int(camera(self.__class__.SHAPE_SIZE_ADJUST*max(self.__class__.IMAGE.get_size()))),
                               math.ceil(camera(5)))

    def move(self):
        ...
    def fire(self):
        ...
    def interact(self):
        ...
    def idle(self):
        ...
    
    

    
    
    




