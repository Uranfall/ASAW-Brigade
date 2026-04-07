import math

import pygame.draw

import shared_utility
from Entity import Entity
from graphics.graphics_utility import Camera


class EntityProp(Entity):
    def __init__(self, relative_position: tuple[int, int], rotation: float, parent: Entity):
        super().__init__(relative_position, rotation)
        self.parent = parent

    def get_real_position(self):
        if isinstance(self.parent, EntityProp):
            parent_pos = self.parent.get_real_position()
        else:
            parent_pos = self.parent.position
        pos = shared_utility.rotate_vector(self.position, self.parent.rotation)
        return pos[0]+parent_pos[0], pos[1]+parent_pos[1]


class GlobalPosEntityProp(EntityProp):

    """
    The same as EntityProp, but stores the global position instead of the one relative to the parent.
    """

    def __init__(self, relative_position: tuple[int, int], rotation: float, parent: Entity):

        super().__init__(relative_position, rotation, parent)
        self.position = super().get_real_position()

    def get_real_position(self):
        return self.position


class MouseTail(GlobalPosEntityProp):

    SEGMENT_COUNT = 20
    SEGMENT_WIDTH_CURVE = shared_utility.ValueCurve((10, 0), (8, 0.6), (1, 1))
    SEGMENT_DISTANCE = 10
    COLOR = (150, 70, 20)

    def __init__(self, relative_position: tuple[int, int],
                 rotation: float,
                 parent: Entity,
                 segment_count=SEGMENT_COUNT):

        if isinstance(parent, EntityProp):
            self.relative_pos = None
        else:
            self.relative_pos = relative_position

        super().__init__(relative_position, rotation, parent)

        self.index = self.SEGMENT_COUNT - segment_count

        if segment_count > 1:
            self.next = self.__class__((0, self.SEGMENT_DISTANCE),
                                       rotation,
                                       self,
                                       segment_count-1)
        else:
            self.next = None

    def get_real_position(self):
        if isinstance(self.parent, EntityProp):
            parent_pos = self.parent.get_real_position()
            return shared_utility.set_distance(self.position, parent_pos, self.SEGMENT_DISTANCE)
        else:
            parent_pos = self.parent.position
            pos = shared_utility.rotate_vector(self.relative_pos, self.parent.rotation)
            return pos[0] + parent_pos[0], pos[1] + parent_pos[1]

    def draw(self, camera: Camera):
        self.position = self.get_real_position()

        size = round(camera(self.SEGMENT_WIDTH_CURVE(self.index/self.SEGMENT_COUNT)))

        screen_pos = camera(*self.position)
        screen_box = -size-camera(self.SEGMENT_COUNT*self.SEGMENT_DISTANCE),\
                     -size-camera(self.SEGMENT_COUNT*self.SEGMENT_DISTANCE),\
                     camera.screen.get_width()+size+camera(self.SEGMENT_COUNT*self.SEGMENT_DISTANCE),\
                     camera.screen.get_height()+size+camera(self.SEGMENT_COUNT*self.SEGMENT_DISTANCE)
        if not (shared_utility.is_within_box(screen_pos, screen_box)):
            return

        pygame.draw.line(camera.screen,
                         self.COLOR,
                         screen_pos,
                         camera(*self.parent.position),
                         size)
        if size < 1:
            return
        if self.next is not None:
            self.next.draw(camera)


