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
from GameData import GameDataLocal


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
        if self.tick_counter == 360:
            self.tick_counter = 0
        else:
            self.tick_counter += 1

def create_grid(WIDTH_START, WIDTH_END, HEIGHT_START, HEIGHT_END):
    grid = []
    for y in range(HEIGHT_START, HEIGHT_END, 200):
        row = []
        for x in range(WIDTH_START, WIDTH_END, 200):
            walkable = True
            row.append(Node(x, y, walkable))
        grid.append(row)
    return grid

def Entity_Handler(entities: list[Entity], units: list[Unit], grid, logic_data):
    for unit in units:
        unit.calc_rotation()
        unit.move(unit.target_pos[0], unit.target_pos[1],logic_data.delta_time)
        if logic_data.tick_counter % unit.attackTickSpeed == 0:
            check_unit_current_action(unit, units, logic_data)
    if logic_data.units_to_delete:
        for unit in logic_data.units_to_delete:
            units.remove(unit)
            entities.remove(unit)
        logic_data.units_to_delete = []
    collision_logic(entities, units)



def check_unit_current_action(unit: Unit, units: list[Unit], logic_data):
    #has a target, no obstacles, is in range
    if unit.targetUnit not in units:
        unit.targetUnit = None
    elif unit.targetUnit is not None and is_within_box(unit.targetUnit.position, unit.get_attack_box()):
        unit.target_pos = unit.position
        if shot_fired(unit.hitChance):
            unit.targetUnit.hp -= unit.damage
        if unit.targetUnit not in logic_data.units_to_delete and unit.targetUnit.hp <= 0:
            logic_data.units_to_delete.append(unit.targetUnit)
            unit.targetUnit = None
        elif unit.targetUnit.hp <= 0:
            unit.targetUnit = None

def collision_x(entity: Entity,unit: Unit):
    old_position = [unit.get_position()[0], unit.get_position()[1] - unit.change_rate[1]]
    if unit != entity and entity.collision == True and boxes_overlap(unit.get_collision_points(),
                                                                     entity.get_collision_points()):
        unit.set_position(old_position)

def collision_y(entity: Entity,unit: Unit):
    old_position = [unit.get_position()[0] - unit.change_rate[0], unit.get_position()[1]]
    if unit != entity and entity.collision == True and boxes_overlap(unit.get_collision_points(),
                                                                     entity.get_collision_points()):
        unit.set_position(old_position)

def collision_logic(entities: list[Entity],units: list[Unit]):
    for unit in units:
        for entity in entities:
            if unit.change_rate[0]>=unit.change_rate[1]:
                collision_y(entity, unit)
                collision_x(entity, unit)
            if unit.change_rate[1]>=unit.change_rate[0]:
                collision_x(entity, unit)
                collision_y(entity, unit)


                #  Example of a debug box:
                #DebugGlobal.ui_data.ui_entities.append(DebugBox(box_unit, stay_alive_for=0.1))
                #DebugGlobal.ui_data.ui_entities.append(DebugBox(box_entity, stay_alive_for=0.1))
                #  ui_data automatically deletes ui_entities that live too long.

def logic_tick(entities: list[Entity], units: list[Unit], grid, logic_data: LOGIC_DATA, game_data: GameDataLocal):
    logic_data.start_new_frame()
    Entity_Handler(entities, units, grid, logic_data)
    if logic_data.tick_counter % 120 == 0:
        game_data.update_player_currency(50, 0)
        game_data.update_player_currency(50, 1)

        print(game_data.get_player_currency(0),game_data.get_player_currency(1))