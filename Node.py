class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.g = 0  # Cost from start
        self.h = 0  # Heuristic cost
        self.parent = None
        self.f = 0  # Total cost