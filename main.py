import pygame

from Entity import Entity

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 30)


def main():
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    entity = Entity((250, 250), 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.draw.circle(screen, (255, 0, 0), (250, 250), 40, 5)

        entity.draw(screen)

        text_surface = FONT.render(str(clock.get_fps()), False, (0, 0, 0))

        screen.blit(text_surface, (0, 0))

        pygame.display.update()
        screen.fill((10, 100, 10))
        clock.tick(60)


if __name__ == '__main__':
    main()

