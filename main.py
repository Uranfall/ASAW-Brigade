import pygame


def main():
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.draw.circle(screen, (255, 0, 0), (250, 250), 40, 5)

        pygame.display.update()
        screen.fill(0)
        clock.tick(60)


if __name__ == '__main__':
    main()

