

class Command:

    GO_TO = 'go_to'
    TARGET = 'target' #sends unit id and unit id for the targeted unit
    ATTACK = 'attack' #unit made a successful attack against another, send unit id of the hit unit and damage
    COLLISION = 'collision' #collision logic, sends unit id and the adjusted position
    DEATH = 'death' #sends a unit id and tells the client to delete it from the list and display the apropriate vfx
    SPAWN = 'spawn' #sends a unit id, unit type and position (can call the spawn function in main, needs adjustment)
    DISCONNECT = 'disconnect'  #client sends this before disconnecting

    def __init__(self, name: str, data: str, unit_id: int = -1):
        self.name = name
        self.data = data
        self.unit_id = unit_id

    def __str__(self):
        return f'{self.name}:{self.unit_id}:{self.data}'

    @staticmethod
    def from_string(string: str):
        name, unit_id, data = string.split(':')
        return Command(name, data, int(unit_id))
