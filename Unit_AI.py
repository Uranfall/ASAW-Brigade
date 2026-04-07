import pygame
from UnitClass import Unit
from logic_utility import NavNode
# check what action is the unit doing right now, call the apropriate function


# all the functions for the bots to actually do stuff
def calc_path(): #find shortest path from closest node to the closest node at the destination
    ...
def find_closest_node(navNodes: list[NavNode]): #finds a nav node closest to the Unit and sets it as target_pos
    for navNode in navNodes:
        ...
def calc_vision():
    ...

def path_clear(positionA: tuple(int,int) ):
    ...