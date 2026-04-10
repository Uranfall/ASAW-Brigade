import DebugGlobal
from logic_utility import *
import pygame
import time

from graphics.Debug_Entities import DebugBox
from graphics.graphics_utility import Camera
from UnitClass import Unit
from Entity import Entity
from graphics.graphics_main import UIData
from shared_utility import boxes_overlap


#this file is for updating unit actions every tick, independent from any inputs, inputs are handled by logic utility
#handle any kind of changes in the game, be it
class logic_data:
    def __init__(self):
        self.delta_time = 0
        self.tick_counter = 0
        self.previous_frame = time.time()

    def start_new_frame(self):
        self.delta_time = time.time()-self.previous_frame
        self.previous_frame = time.time()
        if self.tick_counter == 60:
            self.tick_counter = 0
        else:
            self.tick_counter += 1

def create_grid(GRID_HEIGHT, GRID_WIDTH):
    grid = []
    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            walkable = True
            # Add some obstacles
            if (x == 5 and 3 <= y <= 10) or (x == 10 and 3 <= y <= 10):
                walkable = False
            row.append(Node(x, y, walkable))
        grid.append(row)
    return grid


def Entity_Handler(entities: list[Entity], units: list[Unit]):
    for unit in units:
        unit.calc_rotation()
        unit.calc_movement()
    collision_logic(entities, units)


all_act_types = []
def check_unit_current_action(unit: Unit):
    current_act = unit.act_list[0]

    if current_act in all_act_types:
        performing_act = getattr(unit, current_act)
        performing_act()
    else:
        unit.idle()

def collision_logic(entities: list[Entity],units: list[Unit]):
    for unit in units:
        for entity in entities:
            old_position = unit.get_position()
            unit.set_position( (unit.get_position()[0]+unit.change_rate[0],unit.get_position()[1]) )
            if unit!=entity and entity.collision==True and boxes_overlap(unit.get_collision_points(), entity.collision_points):
                print("triggered x" + str(unit.get_position()))
                unit.set_position(old_position)

            old_position = unit.get_position()
            unit.set_position((unit.get_position()[0], unit.get_position()[1] + unit.change_rate[1]))
            if unit != entity and entity.collision == True and boxes_overlap(unit.get_collision_points(), entity.collision_points):
                print("triggered y" + str(unit.get_position()))
                unit.set_position(old_position)


                #  Example of a debug box:
                #DebugGlobal.ui_data.ui_entities.append(DebugBox(box_unit, stay_alive_for=0.1))
                #DebugGlobal.ui_data.ui_entities.append(DebugBox(box_entity, stay_alive_for=0.1))
                #  ui_data automatically deletes ui_entities that live too long.

def logic_tick(entities: list[Entity], units: list[Unit]):
    Entity_Handler(entities, units)