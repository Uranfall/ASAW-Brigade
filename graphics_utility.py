import pygame

from shared_utility import sign


def invert_y(*args):
    return args[0], -args[1], *args[2:]


class Camera:
    max_zoom = 10.0
    min_zoom = 0.025
    default_screen_size = 500

    def __init__(self, position: list[float, float], zoom: float, screen: pygame.display):
        self.tmp_offset = [0, 0]
        self.position = position
        self.zoom = zoom
        self.screen = screen

    def get_zoom(self):
        return self.zoom*min(self.screen.get_size())/self.__class__.default_screen_size

    def __call__(self, *args: float):
        """
        Gets values and adjusts.
        """
        zoom = self.get_zoom()
        if len(args) > 1:
            args = args[0]+self.position[0]+self.tmp_offset[0], \
                   args[1]+self.position[1]+self.tmp_offset[1],\
                   *args[2:]
        size = self.screen.get_size()[0]/2, -self.screen.get_size()[1]/2
        return invert_y(*(args[i]*zoom + (0 if i > 1 else size[i]) for i in range(len(args)))) \
            if len(args) != 1 else args[0]*zoom

    def screen_to_global(self, *args: float):
        zoom = self.get_zoom()
        size = self.screen.get_size()[0]/2, -self.screen.get_size()[1]/2
        args = invert_y(*args)
        args = tuple((args[i] - (0 if i > 1 else size[i]))/zoom for i in range(len(args))) \
            if len(args) != 1 else args[0]/zoom
        if len(args) > 1:
            args = args[0] - self.position[0] - self.tmp_offset[0], \
                   args[1] - self.position[1] - self.tmp_offset[1], \
                   *args[2:]
        return args

    def adjust_zoom(self,
                    amount: float,
                    mouse_pos: tuple[float, float] | list[float, float] = None):
        if mouse_pos is None:
            global_mouse = self.position
        else:
            global_mouse = self.screen_to_global(mouse_pos[0],
                                                 mouse_pos[1])

        self.zoom = max(self.__class__.min_zoom, min(self.__class__.max_zoom, self.zoom+self.zoom*0.1*amount))

        if mouse_pos is None:
            global_mouse2 = self.position
        else:
            global_mouse2 = self.screen_to_global(mouse_pos[0],
                                                  mouse_pos[1])
        offset = global_mouse2[0]-global_mouse[0], global_mouse2[1]-global_mouse[1]
        self.position[0] += offset[0]
        self.position[1] += offset[1]

    def adjust_position(self, amount: list[float, float], multiply=-1):
        amount = invert_y(*amount)
        self.tmp_offset[0] = amount[0]*multiply/self.get_zoom()
        self.tmp_offset[1] = amount[1]*multiply/self.get_zoom()

    def apply(self):
        self.position[0] += self.tmp_offset[0]
        self.position[1] += self.tmp_offset[1]
        self.tmp_offset = [0, 0]

