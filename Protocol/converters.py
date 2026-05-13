from Entity import Entity
from graphics.Ground import Ground
from Entities.Units import *
from Entities.Bonus import *
from VFX import *


def string_to_entity(string: str) -> Entity:
    list_of_stats = string[1:-1].split(';')
    stats = dict()
    for key, value in map(lambda stat: (stat[:3], stat[3:]), list_of_stats):
        stats.update({key: value})
    try:
        entity = eval(stats['cls']+f'(({stats["pos"]}), {stats["rot"]})')
    except TypeError:
        entity = eval(stats['cls']+f'()')
    entity.id = int(stats['uid'])
    if isinstance(entity, Unit):
        entity.team = int(stats['plr'])
    return entity
