import pygame

from Entity import Entity
from graphics_utility import Camera

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 30)


def main():
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    main_camera = Camera([0, 0], 1, screen)
    entity = Entity((0, 0), 0)

    mouse_pos = pygame.mouse.get_pos()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEWHEEL:
                main_camera.adjust_zoom(event.y)

        if pygame.mouse.get_pressed()[1]:
            new_mouse = pygame.mouse.get_pos()
            main_camera.adjust_position([mouse_pos[0]-new_mouse[0], mouse_pos[1]-new_mouse[1]])
        else:
            main_camera.apply()
            mouse_pos = pygame.mouse.get_pos()

        pygame.draw.circle(screen, (255, 0, 0), main_camera(250, 0), int(main_camera(40)), int(main_camera(5)))
        entity.draw(screen, main_camera)
        text_surface = FONT.render(str(clock.get_fps()), False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

        pygame.display.update()
        screen.fill((10, 100, 10))
        clock.tick(60)


if __name__ == '__main__':
    main()

