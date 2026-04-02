import Unit
import pygame


act_list = list["move", "fire", "interact"]


# check what action is the unit doing right now, call the apropriate function

def check_unit_current_action(unit: Unit):
    current_act = unit.act_queue[0]

    if current_act in act_list:
        performing_act = getattr(unit, current_act)
        performing_act()
    else:
        unit.idle()


# all the functions for the bots to actually do stuff
def calc_path(unit: Unit): #find shortest path from closest node to the closest node at the destination
    ...
def find_closest_node(unit: Unit): #finds a nav node closest to the Unit and sets it as target_pos
    ...
def calc_movement_and_rotation(unit: Unit):
    ...
def calc_vision(unit:Unit):
    ...

