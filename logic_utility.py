from Entity import Entity
#navigation: UNIT -> NavNode -> find a path between them -> stop at closet NavNode from the click that isnt abstracted -> walk towards coordinates


def calculate_route_from(entity: Entity, target: Entity, game_state) -> list[tuple[int, int]]:
    ...
class NavNode:
    def __init__(self, position: tuple[int,int])

