import logic_utility
import pygame
import time
from UnitClass import Unit
from Entity import Entity
from graphics.graphics_main import UIData


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


def logic_tick(entities: list[Entity], units: list[Unit]):
    Entity_Handler(entities, units)