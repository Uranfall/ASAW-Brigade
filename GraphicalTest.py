
import pygame

import DebugGlobal
from Entity import Entity
from graphics.graphics_main import UIData, ui_tick
from graphics.graphics_utility import CinematicCamera
from shared_utility import lerp, ValueCurve
from graphics.UI_Entities import Text


def main():

    ui_data = UIData(pygame.display.set_mode((500, 500), pygame.RESIZABLE))
    keyframes = ValueCurve(({'target_position': [0, 0], 'zoom': 1}, 0),
                           ({'target_position': [0, 0], 'zoom': 1}, 1),
                           ({'target_position': [0, 200], 'zoom': 1}, 1.1),
                           ({'target_position': [0, 200], 'zoom': 1}, 2),
                           ({'target_position': [0, 0], 'zoom': 1}, 2.1),
                           ({'target_position': [0, 0], 'zoom': 1}, 3),
                           ({'zoom': 0.5}, 4),
                           ({'zoom': 0.5}, 5),
                           ({'zoom': 2}, 6),
                           )
    ui_data.camera = CinematicCamera([0, 0], 1, ui_data.screen, keyframes=keyframes)
    DebugGlobal.ui_data = ui_data
    entities: list[Entity] = [Entity((0, 0), 0)]

    run = True
    while run:
        ui_out = ui_tick(ui_data, entities)
        run = ui_out.run
        ui_data.camera.animate(ui_data.delta_time)


if __name__ == '__main__':
    obj1 = Entity((0, 0), 1)
    print(obj1.position)
    obj2 = Entity((0, 10), 1)
    print(obj2.position)
    obj3 = lerp(obj1, obj2, 0.5)
    print(obj3.position)

    t = Text((0, 0), 0, 'hello!', (255, 255, 0))
    t2 = {'text': 'bye!', 'rotation': 90}
    lerp(t, t2, 1, overwrite_object=True)
    print(t.text, t.rotation)
    main()
