from __future__ import annotations
from Entity import Entity
from UnitClass import Unit
#navigation: UNIT -> NavNode -> find a path between them -> stop at closet NavNode from the click that isnt abstracted -> walk towards coordinates



class NavNode:
    def __init__(self, position: tuple[int,int],
                 connections: list[NavNode]):
        self.position = position
        self.connections = connections

all_act_types = []
def check_unit_current_action(unit: Unit):
    current_act = unit.act_list[0]

    if current_act in all_act_types:
        performing_act = getattr(unit, current_act)
        performing_act()
    else:
        unit.idle()

def collision_logic():
    ...

