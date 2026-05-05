import DebugGlobal
from logic_utility import *
import pygame
import time

from graphics.Debug_Entities import DebugBox
from graphics.graphics_utility import Camera
from UnitClass import *
from Entity import Entity
from graphics.graphics_main import UIData
from shared_utility import boxes_overlap


#this file is for updating unit actions every tick, independent from any inputs, inputs are handled by logic utility
#handle any kind of changes in the game, be it
class LOGIC_DATA:
    def __init__(self):
        self.delta_time = 0
        self.units_to_delete = []
        self.tick_counter = 0
        self.previous_frame = time.time()

    def start_new_frame(self):
        self.delta_time = time.time()-self.previous_frame
        self.previous_frame = time.time()
        if self.tick_counter == 60:
            self.tick_counter = 0
        else:
            self.tick_counter += 1

def create_grid(WIDTH_START, WIDTH_END, HEIGHT_START, HEIGHT_END):
    grid = []
    for y in range(HEIGHT_START, HEIGHT_END, 50):
        row = []
        for x in range(WIDTH_START, WIDTH_END, 50):
            walkable = True
            row.append(Node(x, y, walkable))
        grid.append(row)
    return grid


def get_current_node(unit: Unit, grid):
    first_node = None
    for row in grid:
        for node in row:
            if first_node is None:
                first_node = node
            if node.walkable and is_within_box([node.x, node.y], unit.get_collision_points()):
                unit.set_position([node.x, node.y])
                unit.target_position = unit.position
                return node
    return first_node

def Entity_Handler(entities: list[Entity], units: list[Unit], grid, logic_data):
    for unit in units:
        unit.calc_rotation()
        unit.move(unit.target_pos[0], unit.target_pos[1])
        check_unit_current_action(unit, entities, logic_data)
    if logic_data.units_to_delete:
        for unit in logic_data.units_to_delete:
            units.remove(unit)
            logic_data.units_to_delete.remove(unit)
    #collision_logic(entities, units)



def check_unit_current_action(unit: Unit, entities: list[Entity], logic_data):
    #has a target, no obstacles, is in range
    if unit.targetUnit is not None and path_clear(unit.get_position(), unit.targetUnit.get_position(), entities) and is_within_box(unit.targetUnit.position, unit.attackRange):
        if shot_fired():
            unit.targetUnit.hp -= unit.damage
        if unit.targetUnit.hp <= 0:
            unit.targetUnit = None
            logic_data.units_to_delete.append(unit.targetUnit)


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

def logic_tick(entities: list[Entity], units: list[Unit], grid, logic_data: LOGIC_DATA):
    Entity_Handler(entities, units, grid, logic_data)