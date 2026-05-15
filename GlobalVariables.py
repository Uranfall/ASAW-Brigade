import pygame

from shared_utility import ValueCurve

pygame.init()
pygame.font.init()

TEAM_COLORS = ((0, 0, 220), (220, 0, 0), (0, 220, 0), (220, 220, 0))
FONT = pygame.font.SysFont('Arial', 30)
TEXT_RED_CURVE = ValueCurve(((255, 100, 50), 0.1),
                            ((20, 20, 20), 0.2),
                            ((255, 100, 50), 0.3),
                            ((255, 100, 50), 0.5),
                            ((20, 20, 20), 0.6),
                            ((20, 20, 20), 0.7),
                            ((255, 100, 50), 0.8),
                            ((20, 20, 20), 0.9),
                            ((255, 100, 50), 1),)
reinforcement_time = 60 * 5
# reinforcement_time = 30
