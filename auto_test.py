import random
from typing import Callable
from Entity import Entity
from Protocol import converters
from graphics.Ground import Ground
from Entities.Units import *
from Entities.Bonus import *
from VFX import *


ENTITIES_TO_TEST = [Entity, Ground, Mouse, Soldier, Tank, VFX, Explosion, GunFire]


def test_string_to_entity():
    entity = random.choice(ENTITIES_TO_TEST)
    if issubclass(entity, Ground):
        entity = entity()
    elif issubclass(entity, Unit):
        entity = entity((random.uniform(-100000, 100000), random.uniform(-100000, 100000)),
                        random.uniform(-360, 360), False, random.randint(0, 1))
    else:
        entity = entity((random.uniform(-100000, 100000), random.uniform(-100000, 100000)),
                        random.uniform(-360, 360))
    new_entity = converters.string_to_entity(str(entity))
    if math.dist(new_entity.position, entity.position) > 0.1 or\
            abs(new_entity.rotation - entity.rotation) > 0.1 or new_entity.id != entity.id:
        print(entity, new_entity)
        return False
    return True


def run_test(randomized_test: Callable, message: str = 'running test', amount: int = 1000):
    print(f'{message}.', end='')
    failure = 0
    errors = 0
    for test_num in range(amount):
        if test_num % 10 == 0:
            print(f'\r{message}, {round(test_num/amount*100)}% there.', end='')
        try:
            if not randomized_test():
                failure += 1
        except Exception as e:
            print(e)
            failure += 1
            errors += 1
    print(f'\rran {amount} tests, {failure} failed.\n'
          f'{round(failure/amount*100, 2)}% failure'
          + ('.' if failure == 0 else f', of them {round(errors/failure*100, 2)}% error.'))
    return failure/amount


if __name__ == '__main__':
    # run_test(lambda: random.randint(0, 100), amount=1000000)
    run_test(test_string_to_entity, 'testing string to entity', amount=1000)




