import math
import random
import time

import pygame.draw

import shared_utility
from Entity import Entity
from graphics.UI_Entities import UIEntity
from graphics.graphics_utility import Camera
from shared_utility import ValueCurve


class VFX(UIEntity):
    LIFETIME = 20

    def __init__(self, position: tuple[int, int], rotation: float, time_offset=0):
        super().__init__(position, rotation, time_offset)


class Particle(VFX):
    COLOR_CURVE = ValueCurve(((0, 0, 0), 0), ((1, 1, 1), 1))
    SCALE_CURVE = ValueCurve((0, 0), (1, 1))
    DRAG = 0.1
    LIFETIME = 1

    def __init__(self, position: tuple[int, int], speed: float, rotation: float = None):
        if rotation is None:
            rotation = random.uniform(0, 360)
        super().__init__(position, rotation)
        self.speed = speed
        self.last_update = time.time()

    def draw(self, camera: Camera):
        size = math.ceil(camera(self.__class__.SCALE_CURVE(self.get_progress())))
        box = -size, -size, camera.screen.get_width()+size, 500*camera.screen.get_height()+size
        if shared_utility.is_within_box(camera(*self.position), box):
            pygame.draw.circle(camera.screen,
                               tuple(map(int, self.__class__.COLOR_CURVE(self.get_progress()))),
                               camera(*self.position),
                               size)

    def move(self):
        dt = time.time() - self.last_update
        self.last_update = time.time()

        direction = shared_utility.angle_to_vector(self.rotation, self.speed * dt)
        self.position = [self.position[0] + direction[0], self.position[1] + direction[1]]
        self.speed /= 1 + self.__class__.DRAG*dt


class ParticleHaving(VFX):
    def __init__(self, position: tuple[int, int], rotation: float):
        super().__init__(position, rotation)
        self.particles = []

    def draw(self, camera: Camera):
        for particle in self.particles[:]:
            particle.draw(camera)
            particle.move()
            if particle.get_progress() > 1:
                self.particles.remove(particle)


class ExplosionParticle(Particle):
    COLOR_CURVE = ValueCurve(((255, 255, 255), 0), ((255, 200, 50), 0.2), ((255, 100, 0), 1))
    SCALE_CURVE = ValueCurve((50, 0), (10, 0.8), (0, 1))
    LIFETIME = 0.5


class Explosion(ParticleHaving):
    START_AMOUNT = 100
    FINAL_AMOUNT = 400

    MIN_SPEED = 30.0
    MAX_SPEED = 2000.0

    BURNING_TIME = 0.15
    PARTICLE_TYPE = ExplosionParticle

    SHOOT_OUT_CHANGE = 0.5
    SHOOT_OUT_FACTOR = 1.5

    def __init__(self, position: tuple[int, int], rotation: float):
        super().__init__(position, rotation)
        self.particles = [self.__class__.PARTICLE_TYPE(self.position,
                                                       random.uniform(self.__class__.MIN_SPEED,
                                                                      self.__class__.MAX_SPEED)
                                                       * (1 if random.random()<self.__class__.SHOOT_OUT_CHANGE
                                                          else self.__class__.SHOOT_OUT_FACTOR))
                          for _ in range(self.__class__.START_AMOUNT)]

    def get_burning_progress(self):
        return self.get_age() / self.__class__.BURNING_TIME

    def draw(self, camera: Camera):
        super().draw(camera)
        if self.get_burning_progress() < 1:
            self.particles.extend([self.__class__.PARTICLE_TYPE(self.position,
                                                            random.uniform(self.__class__.MIN_SPEED,
                                                                           self.__class__.MAX_SPEED))
                               for _ in range(int(shared_utility.lerp(0,
                                                                      self.__class__.FINAL_AMOUNT,
                                                                      self.get_burning_progress())
                                                  - len(self.particles)))])
