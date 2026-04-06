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
    DRAG = 5
    LIFETIME = 1
    ROTATION_WIGGLE = 0.0
    DEFAULT_ACCELERATION = 0.0

    def __init__(self, position: tuple[int, int], speed: float, rotation: float = None):
        if rotation is None:
            rotation = random.uniform(0, 360)
        super().__init__(position, rotation)
        self.speed = speed
        self.last_update = time.time()

    def draw(self, camera: Camera):
        size = math.ceil(camera(self.SCALE_CURVE(self.get_progress())))
        box = -size, -size, camera.screen.get_width()+size, 500*camera.screen.get_height()+size
        if shared_utility.is_within_box(camera(*self.position), box):
            pygame.draw.circle(camera.screen,
                               tuple(map(int, self.COLOR_CURVE(self.get_progress()))),
                               camera(*self.position),
                               size)

    def move(self):
        dt = time.time() - self.last_update
        self.last_update = time.time()

        direction = shared_utility.angle_to_vector(self.rotation, self.speed * dt)
        self.position = [self.position[0] + direction[0], self.position[1] + direction[1]]
        self.speed /= 1 + self.DRAG*dt

        self.speed += self.DEFAULT_ACCELERATION*dt
        self.rotation += random.uniform(-self.ROTATION_WIGGLE, self.ROTATION_WIGGLE)*dt


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


class ExplosionCrater(Entity):
    IMAGE = pygame.image.load('./Sprites/Objects/crater.png')


class ExplosionParticle(Particle):
    COLOR_CURVE = ValueCurve(((255, 220, 100), 0), ((255, 200, 50), 0.2), ((255, 100, 0), 1))
    SCALE_CURVE = ValueCurve((50, 0), (10, 0.8), (0, 1))
    LIFETIME = 0.5


class ExplosionSmokeParticle(Particle):
    COLOR_CURVE = ValueCurve(((255, 220, 100), 0), ((255, 200, 50), 0.1), ((100, 100, 100), 0.2), ((50, 50, 50), 1))
    SCALE_CURVE = ValueCurve((70, 0), (60, 0.1), (30, 0.5), (10, 0.8), (0, 1))
    LIFETIME = 3
    DRAG = 10


class Explosion(ParticleHaving):
    START_AMOUNT = 100
    FINAL_AMOUNT = 400
    SMOKE_FACTOR = 0.15

    MIN_SPEED = 30.0
    MAX_SPEED = 2000.0

    BURNING_TIME = 0.15

    PARTICLE_TYPE = ExplosionParticle
    SMOKE_PARTICLE = ExplosionSmokeParticle

    SHOOT_OUT_CHANGE = 0.3
    SHOOT_OUT_FACTOR = 1.5

    def __init__(self, position: tuple[int, int], rotation: float):
        super().__init__(position, rotation)
        self.particles = [self.get_new_particle() for _ in range(self.START_AMOUNT)]

    def get_burning_progress(self):
        return self.get_age() / self.BURNING_TIME

    def get_new_particle_count(self):
        if self.get_burning_progress() < 1:
            return int(shared_utility.lerp(0,
                                           self.FINAL_AMOUNT,
                                           self.get_burning_progress()) - len(self.particles))
        return 0

    def get_new_particle(self):
        if random.random() >= self.SMOKE_FACTOR:
            return self.PARTICLE_TYPE(self.position, random.uniform(self.MIN_SPEED,
                                                                    self.MAX_SPEED)
                                                * (self.SHOOT_OUT_FACTOR if random.random()<self.SHOOT_OUT_CHANGE
                                                   else 1))

        return self.SMOKE_PARTICLE(self.position, random.uniform(self.MIN_SPEED, self.MAX_SPEED))

    def draw(self, camera: Camera):
        super().draw(camera)
        self.particles.extend([self.get_new_particle() for _ in range(self.get_new_particle_count())])
