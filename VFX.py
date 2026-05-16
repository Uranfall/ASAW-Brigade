import math
import random
import time

import pygame.draw

import shared_utility
from Entity import Entity
from graphics.UI_Entities import UIEntity
from graphics.graphics_utility import Camera
from shared_utility import ValueCurve, lerp


class VFX(UIEntity):
    NAME = 'FX'
    LIFETIME = 20
    RENDER_LAYER = 9

    def __init__(self, position: tuple[float, float], rotation: float, time_offset=0):
        super().__init__(position, rotation, time_offset)


class Particle(VFX):
    COLOR_CURVE = ValueCurve(((0, 0, 0), 0), ((1, 1, 1), 1))
    SCALE_CURVE = ValueCurve((0, 0), (1, 1))
    DRAG = 5
    LIFETIME = 1
    ROTATION_WIGGLE = 0.0
    DEFAULT_ACCELERATION = 0.0


    def __init__(self, position: tuple[float, float], speed: float, rotation: float = None):
        if rotation is None:
            rotation = random.uniform(0, 360)
        super().__init__(position, rotation)
        self.speed = speed
        self.last_update = time.time()

    def get_color(self):
        return tuple(map(int, self.COLOR_CURVE(self.get_progress())))

    def draw(self, camera: Camera):
        size = math.ceil(camera(self.SCALE_CURVE(self.get_progress())))
        box = -size, -size, camera.screen.get_width()+size, 500*camera.screen.get_height()+size
        if shared_utility.is_within_box(camera(*self.position), box):
            pygame.draw.circle(camera.screen,
                               self.get_color(),
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
    NAME = 'PH'

    def __init__(self, position: tuple[float, float], rotation: float):
        super().__init__(position, rotation)
        self.particles = []

    def draw(self, camera: Camera):
        for particle in self.particles[:]:
            particle.draw(camera)
            particle.move()
            if particle.get_progress() > 1:
                self.particles.remove(particle)


class ExplosionCrater(Entity):
    NAME = 'CR'
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
    NAME = 'EX'
    START_AMOUNT = 100
    FINAL_AMOUNT = 400
    SMOKE_FACTOR = 0.15

    MIN_SPEED = 30.0
    MAX_SPEED = 2000.0

    BURNING_TIME = 0.15

    PARTICLE_TYPE = ExplosionParticle
    SMOKE_PARTICLE = ExplosionSmokeParticle

    SHOOT_OUT_CHANCE = 0.3
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
                                                * (self.SHOOT_OUT_FACTOR if random.random()<self.SHOOT_OUT_CHANCE
                                                   else 1))

        return self.SMOKE_PARTICLE(self.position, random.uniform(self.MIN_SPEED, self.MAX_SPEED))

    def draw(self, camera: Camera):
        super().draw(camera)
        self.particles.extend([self.get_new_particle() for _ in range(self.get_new_particle_count())])


class ColorfulExplosionParticle(ExplosionParticle):
    COLOR_CURVE = ValueCurve(((255, 0, 0), 0),
                             ((255, 255, 0), 60),
                             ((0, 255, 0), 120),
                             ((0, 0, 255), 180),
                             ((0, 0, 255), 250),
                             ((255, 0, 255), 300),
                             ((255, 0, 0), 360))
    SCALE_CURVE = ValueCurve((30, 0), (20, 0.1), (15, 0.5), (10, 0.8), (0, 1))

    def __init__(self, position: tuple[float, float], speed: float):
        super().__init__(position, speed)
        self.hue = random.random()*360
        self.value = 1
        self.saturation = random.random()

    def get_color(self):
        color = self.COLOR_CURVE(self.hue)
        average = lerp(sum(color)//3, self.value*255, 0.5)  # not accurate color calculation.
        return tuple(map(lambda val: int((lerp(average, val, self.saturation))*self.value), self.COLOR_CURVE(self.hue)))


class ColorfulExplosion(Explosion):
    NAME = "CE"
    SMOKE_FACTOR = 0
    COLOR_CURVE = ValueCurve(((255, 220, 100), 0), ((255, 200, 50), 0.3), ((100, 100, 100), 0.6), ((50, 50, 50), 1))
    PARTICLE_TYPE = ColorfulExplosionParticle
    FINAL_AMOUNT = 100
    MAX_SPEED = 1000


class ColorfulFire(ColorfulExplosion):
    NAME = "CF"
    FINAL_AMOUNT = 500
    BURNING_TIME = 15


class ShotEffect(VFX):
    NAME = 'SX'

    def __init__(self, position: tuple[int, int], rotation: float, distance=1000.0):
        super().__init__(position, rotation)


class GunFireParticle(ExplosionParticle):
    SCALE_CURVE = ValueCurve((8, 0), (6, 0.1), (5, 0.5), (3, 0.8), (0, 1))
    DRAG = 40


class GunFireSmokeParticle(ExplosionSmokeParticle):
    SCALE_CURVE = ValueCurve((10, 0), (8, 0.1), (6, 0.5), (3, 0.8), (0, 1))
    LIFETIME = 1
    DRAG = 40


class GunFire(Explosion, ShotEffect):
    NAME = "GF"

    MIN_SPEED = 10
    MAX_SPEED = 500
    FINAL_AMOUNT = 20
    START_AMOUNT = 10
    BURNING_TIME = 0.05
    PARTICLE_TYPE = GunFireParticle
    SMOKE_PARTICLE = GunFireSmokeParticle

    def __init__(self, position: tuple[int, int], rotation: float, distance=1000.0):
        super().__init__(position, rotation)


class SmokeTrail(ParticleHaving, ShotEffect):
    NAME = "ST"

    PARTICLE_TYPE = GunFireSmokeParticle
    PARTICLE_DISTANCE = 5.0
    LIFETIME = 10

    def __init__(self, position: tuple[int, int], rotation: float, distance=1000.0):
        super().__init__(position, rotation)
        pos = list(self.position)
        direction = shared_utility.angle_to_vector(rotation, self.PARTICLE_DISTANCE)
        self.particles = []
        for _ in range(int(distance/self.PARTICLE_DISTANCE)):
            self.particles.append(self.PARTICLE_TYPE((pos[0], pos[1]),
                                                     rotation+random.randint(-90, 90)))
            pos[0] += direction[0]
            pos[1] += direction[1]


class BloodParticle(Particle):
    COLOR_CURVE = ValueCurve(((175, 50, 50), 0), ((150, 50, 50), 0.2), ((75, 30, 30), 1))
    SCALE_CURVE = ValueCurve((20, 0), (15, 0.25), (0, 1))
    LIFETIME = 5
    DRAG = 5


class BloodSplatter(Explosion):
    NAME = "BS"
    RENDER_LAYER = 1
    PARTICLE_TYPE = BloodParticle
    FINAL_AMOUNT = 70
    START_AMOUNT = 35
    SMOKE_FACTOR = 0.0
    MAX_SPEED = 250
    BURNING_TIME = 1
    SHOOT_OUT_FACTOR = 2
    SHOOT_OUT_CHANCE = 0.4


class SmallBloodParticle(Particle):
    COLOR_CURVE = ValueCurve(((175, 50, 50), 0), ((150, 50, 50), 0.2), ((75, 30, 30), 1))
    SCALE_CURVE = ValueCurve((10, 0), (9, 0.25), (0, 1))
    LIFETIME = 2
    DRAG = 5


class SmallBloodSplatter(Explosion):
    NAME = "SB"
    RENDER_LAYER = 1
    PARTICLE_TYPE = SmallBloodParticle
    FINAL_AMOUNT = 40
    START_AMOUNT = 25
    SMOKE_FACTOR = 0.0
    MAX_SPEED = 100
    BURNING_TIME = 0.25
    SHOOT_OUT_FACTOR = 2
    SHOOT_OUT_CHANCE = 0.4


class TankExhaustParticle(Particle):
    COLOR_CURVE = ValueCurve(((100, 100, 100), 0), ((200, 200, 200), 1))
    SCALE_CURVE = ValueCurve((1, 0), (2.5, 0.25), (1, 0.8), (0, 1))
    LIFETIME = 0.5
    ROTATION_WIGGLE = 5
    DEFAULT_ACCELERATION = 1

    def __init__(self, position: tuple[float, float], speed: float, rotation: float = 0):
        super().__init__(position, speed, rotation)


class TankExhaust(ParticleHaving):
    EMISSION_RATE = 50  # particles per second
    MIN_SPEED = 50
    MAX_SPEED = 150

    def __init__(self, position: tuple[float, float], rotation: float):
        super().__init__(position, rotation)
        self.last_emission = time.time()

    def check_emit(self):
        if time.time()-self.last_emission > (1+random.random())/2/self.EMISSION_RATE:
            self.particles.append(TankExhaustParticle(self.position,
                                                      random.randint(self.MIN_SPEED, self.MAX_SPEED),
                                                      self.rotation-180+random.randint(-25, 25),
                                                      ))
            self.last_emission = time.time()
