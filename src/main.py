import sys
import pygame

from src.button import Button

from .constants import (
    BLACK,
    WHITE,
    GREEN,
    WIDTH,
    HEIGHT,
    FPS
)
from .maze import Maze

pygame.init()
pygame.font.init()


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder")

CLOCK = pygame.time.Clock()

title_font = pygame.font.SysFont("Verdana", 40, True)
title_surf = title_font.render("PATHFINDER", True, BLACK)


def main() -> None:
    """
    Start here
    """

    maze = Maze(surface=WINDOW)
    button = Button(
        "Start", "center", HEIGHT - 80,
        background_color=pygame.Color(*GREEN),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=30
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.fill(WHITE)

        WINDOW.blit(title_surf, ((WIDTH - title_surf.get_width()) / 2, 20))
        maze.draw()
        if button.draw(WINDOW):
            solved = maze.solve()
            pygame.time.delay(5000)

        pygame.display.update()
        CLOCK.tick(FPS)
