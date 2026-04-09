import DebugGlobal
import logic_utility
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
            if unit!=entity and entity.collision==True and boxes_overlap(unit.get_collision_points(), entity.collision_points):
                coords = unit.get_position()
                box_unit = unit.get_collision_points()
                box_entity = entity.collision_points
                print(box_unit, box_entity)
                #find which one is needed to be offset and where
                

                unit.set_position([coords[0], coords[1]])

                #  Example of a debug box:
                DebugGlobal.ui_data.ui_entities.append(DebugBox(box_unit, stay_alive_for=0.1))
                DebugGlobal.ui_data.ui_entities.append(DebugBox(box_entity, stay_alive_for=0.1))
                #  ui_data automatically deletes ui_entities that live too long.

def logic_tick(entities: list[Entity], units: list[Unit]):
    Entity_Handler(entities, units)