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

    maze = Maze()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.fill(WHITE)
        maze.draw(WINDOW)

        pygame.display.update()
        CLOCK.tick(FPS)
