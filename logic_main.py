import DebugGlobal
from Entities.Units import Mouse, Tank, Soldier
from logic_utility import *
import pygame
import time

from graphics.Debug_Entities import DebugBox
from graphics.graphics_utility import Camera
from UnitClass import *
from Entity import Entity
from graphics.graphics_main import UIData
from shared_utility import boxes_overlap
from GameData import GameDataLocal, GameDataServer


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


def Entity_Handler(entities: list[Entity],
                   units: list[Unit],
                   grid,
                   logic_data,
                   game_data: GameDataServer):
    for unit in units:
        unit.calc_rotation()
        unit.move(unit.target_pos[0], unit.target_pos[1],logic_data.delta_time)
        if logic_data.tick_counter % unit.attackTickSpeed == 0:
            check_unit_current_action(unit, entities, units, logic_data, game_data)
    if logic_data.units_to_delete:
        for unit in logic_data.units_to_delete:
            units.remove(unit)
            entities.remove(unit)
        logic_data.units_to_delete = []
    collision_logic(entities, units)


def check_unit_current_action(unit: Unit,
                              entities: list[Entity],
                              units: list[Unit],
                              logic_data,
                              game_data: GameDataServer):
    #has a target, no obstacles, is in range
    if unit.targetUnit not in units:
        unit.targetUnit = None
    elif (unit.targetUnit is not None
          and is_within_box(unit.targetUnit.position, scale_box(unit.get_attack_box(), 0.9))):
        unit.target_pos = unit.position
        if shot_fired(unit.hitChance):
            game_data.add_vfx(*unit.get_shooting_effects())
            unit.targetUnit.hp -= unit.damage
        if unit.targetUnit not in logic_data.units_to_delete and unit.targetUnit.hp <= 0:
            game_data.add_vfx(*unit.targetUnit.get_death_effects())
            logic_data.units_to_delete.append(unit.targetUnit)
            unit.targetUnit = None
        elif unit.targetUnit.hp <= 0:
            game_data.add_vfx(*unit.targetUnit.get_death_effects())
            unit.targetUnit = None
    elif unit.MELEE and unit.targetUnit is not None:
        unit.target_pos = unit.targetUnit.position


def collision_x(entity: Entity,unit: Unit):
    old_position = [unit.get_position()[0], unit.get_position()[1] - unit.change_rate[1]*random.uniform(0.8, 1.2)]
    if unit != entity and entity.collision == True and boxes_overlap(unit.get_collision_points(),
                                                                     entity.get_collision_points()):
        unit.set_position(old_position)


def collision_y(entity: Entity,unit: Unit):
    old_position = [unit.get_position()[0] - unit.change_rate[0]*random.uniform(0.8, 1.2), unit.get_position()[1]]
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


def logic_tick(entities: list[Entity], units: list[Unit], grid, logic_data: LOGIC_DATA, game_data: GameDataServer):

    logic_data.start_new_frame()
    for command in game_data.get_commands():
        if command.name == command.ATTACK:
            print('attack')
            game_data.get_unit_by_uid(command.unit_id).targetUnit = game_data.get_unit_by_uid(int(command.data))
        if command.name == command.GO_TO:
            print('move')
            game_data.get_unit_by_uid(command.unit_id).target_pos = tuple(map(float, command.data[1:-1].split(',')))
            game_data.get_unit_by_uid(command.unit_id).targetUnit = None
        if command.name == command.SPAWN:
            print('spawn')
            spawn(game_data, command.team, command.data)
    Entity_Handler(entities, units, grid, logic_data, game_data)
    if time.time()-game_data.get_start_time() < 60*5 and logic_data.tick_counter % 120 == 0:
        game_data.update_player_currency(50, 0)
        game_data.update_player_currency(50, 1)
        game_data.clean_up_vfx()

        print(game_data.get_player_currency(0), game_data.get_player_currency(1))


units_to_spawn = {Mouse.NAME: [Mouse, 250], Soldier.NAME: [Soldier, 500], Tank.NAME: [Tank, 1000]}


def spawn(game_data, player_team, unit: str):
    if units_to_spawn[unit] is None:
        return
    unit = units_to_spawn[unit]
    spawn_points = game_data.get_player_spawns(player_team)
    money = game_data.get_player_currency(player_team)
    if money >= 250:
        game_data.update_player_currency(-unit[1], player_team)
        newUnit = unit[0](spawn_points[0], 90, False, player_team)
        newUnit.current_node = get_closest_node(newUnit.get_position(), game_data.get_grid())
        newUnit.target_node = newUnit.current_node
        # add unit
        game_data.units.append(newUnit)
        game_data.entities.append(newUnit)
        # shift list left, set the next spawn as the one the next unit is going to use
        game_data.shift_player_spawns(player_team)

