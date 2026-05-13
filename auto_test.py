import random
from typing import Callable
from Entity import Entity
from Protocol import converters
from Protocol.Command import Command
from graphics.Ground import Ground
from Entities.Units import *
from Entities.Bonus import *
from VFX import *

test_log = []


ENTITIES_TO_TEST = [Entity, Ground, Mouse, Soldier, Tank, VFX, Explosion, GunFire]


def test_string_to_entity(verbose=False):
    global test_log
    entity = random.choice(ENTITIES_TO_TEST)
    test_log.append(entity)
    if issubclass(entity, Ground):
        entity = entity()
    elif issubclass(entity, Unit):
        entity = entity((random.uniform(-100000, 100000), random.uniform(-100000, 100000)),
                        random.uniform(-360, 360),
                        team=random.randint(0, 1))
    else:
        entity = entity((random.uniform(-100000, 100000), random.uniform(-100000, 100000)),
                        random.uniform(-360, 360))
    test_log.append(entity)
    new_entity = converters.string_to_entity(str(entity))
    if math.dist(new_entity.position, entity.position) > 0.1 or\
            abs(new_entity.rotation - entity.rotation) > 0.1 or new_entity.id != entity.id or \
            str(entity) != str(new_entity):
        if verbose:
            print(entity, new_entity)
        return False
    return True


def test_string_to_command(verbose=False):
    global test_log
    command = random.choice([Command.SPAWN, Command.ATTACK, Command.GO_TO])
    test_log.append(command)
    command = Command(command,
                      str(random.randint(-100, 100)),
                      random.randint(-100, 100))
    test_log.append(command)
    new_command = Command.from_string(str(command))
    if str(new_command) != str(command) or new_command.name != command.name or new_command.unit_id != command.unit_id:
        return False
    return True


def run_test(randomized_test: Callable,
             message: str = 'running test',
             amount: int = 1000,
             verbose=True,
             print_log_threshold=0.2):
    global test_log
    test_log.clear()
    print(f'{message}.', end='')
    failure = 0
    errors = 0
    error_types = dict()
    failure_stats = {}
    for test_num in range(amount):
        if test_num % 10 == 0:
            print(f'\r{message}, {round(test_num/amount*100)}% there.', end='')
        failed = False
        try:
            if not randomized_test(verbose=verbose):
                failed = True
        except Exception as e:
            if verbose:
                if test_log:
                    print(f'\nError happened on {tuple(map(str, test_log))}:')
                else:
                    print('Error without log:')
                print(e)
            failed = True
            errors += 1
            if error_types.get(type(e).__name__):
                error_types[type(e).__name__] += 1
            else:
                error_types[type(e).__name__] = 1
        if failed:
            failure += 1
            for data in test_log:
                if failure_stats.get(str(data)) is None:
                    failure_stats[str(data)] = 1
                else:
                    failure_stats[str(data)] += 1
        test_log.clear()
    print(f'\r{message} is complete.')
    print(f'ran {amount} tests, {failure} failed.\n'
          f'{round(failure/amount*100, 2)}% failure'
          + ('.' if failure == 0 else f', of them {round(errors/failure*100, 2)}% error.'))
    if errors:
        print('list of errors:')
        for error, count in error_types.items():
            print(f' - {error}: {count} ({round(count/errors*100, 2)})%')
    if failure_stats:
        print('log analysis:')
        most_common_info = None
        significant_data = []
        total_logged = sum(failure_stats.values())
        for data, count in failure_stats.items():
            if most_common_info is None or count > failure_stats[most_common_info]:
                most_common_info = data
            if count/failure >= print_log_threshold:
                significant_data.append(data)
        print(f'\rThe data that appeared most in the log is:\n - {most_common_info}:'
              f' {failure_stats[most_common_info]} times '
              f'({round(failure_stats[most_common_info]/failure*100, 2)}% of the amount of tests failed).')
        if significant_data:
            print(f'Full list of data that is more than {print_log_threshold*100}% of the amount of tests failed:')
            for data in sorted(significant_data, key=lambda d: failure_stats[d], reverse=True):
                count = failure_stats[data]
                print(f' - {data}: {count} ({round(count / failure * 100, 2)}%)')
            if len(failure_stats) > len(significant_data) > 0:
                print(f'Hid {len(failure_stats)-len(significant_data)} data that did not pass the threshold.')
        else:
            print(f'No data is more than {print_log_threshold*100}% of the amount of tests failed.')
            print(f'Hid {len(failure_stats)-len(significant_data)}.')
        print('end of log analysis.')
    return failure/amount


if __name__ == '__main__':
    # run_test(lambda verbose: random.randint(0, 100), amount=1000000)
    run_test(test_string_to_entity, 'testing string to entity', amount=1000, verbose=True)
    run_test(test_string_to_command, 'testing string to command', amount=1000, verbose=True)




