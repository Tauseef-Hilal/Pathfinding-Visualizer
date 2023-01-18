import sys
import pygame

from .constants import (
    WHITE,
    WIDTH,
    HEIGHT,
    FPS
)
from .maze import Maze

pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder")

CLOCK = pygame.time.Clock()


def main() -> None:
    """
    Start here
    """

    maze = Maze(surface=WINDOW)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.fill(WHITE)

        maze.draw()
        maze.solve()

        pygame.time.delay(5000)
        pygame.display.update()
        CLOCK.tick(FPS)
