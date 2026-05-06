

class Command:

    GO_TO = 'go_to'
    ATTACK = 'attack'

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
