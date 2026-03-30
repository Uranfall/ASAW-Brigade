import pygame


def invert_y(*args):
    return args[0], -args[1], *args[2:]


class Camera:
    def __init__(self, position: list[float, float], zoom: float, screen: pygame.display):
        self.tmp_offset = [0, 0]
        self.position = position
        self.zoom = zoom
        self.screen = screen

    def __call__(self, *args: float):
        """
        Gets values and adjusts.
        """
        print(args, self.position)
        if len(args) > 1:
            args = args[0]+self.position[0]+self.tmp_offset[0], \
                   args[1]+self.position[1]+self.tmp_offset[1],\
                   *args[2:]
        size = self.screen.get_size()[0]/2, -self.screen.get_size()[1]/2
        return invert_y(*(args[i]*self.zoom + (0 if i > 1 else size[i]) for i in range(len(args)))) \
            if len(args) != 1 else args[0]*self.zoom

    def adjust_zoom(self, amount: float):
        self.zoom += self.zoom*0.1*amount

    def adjust_position(self, amount: list[float, float], multiply=-1):
        amount = invert_y(*amount)
        self.tmp_offset[0] = amount[0]*multiply/self.zoom
        self.tmp_offset[1] = amount[1]*multiply/self.zoom

    def apply(self):
        self.position[0] += self.tmp_offset[0]
        self.position[1] += self.tmp_offset[1]
        self.tmp_offset = [0, 0]

