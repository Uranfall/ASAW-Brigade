from Entity import Entity


def string_to_entity(string: str) -> Entity:
    list_of_stats = string[1:-1].split(';')
    stats = dict()
    for key, value in map(lambda stat: (stat[:3], stat[3:]), list_of_stats):
        stats.update({key: value})
    entity = eval(stats['cls']+f'({stats["pos"]}, {stats["rot"]}, unique_id={stats["uid"]})')
    return entity
