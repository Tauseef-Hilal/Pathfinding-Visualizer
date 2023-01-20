import os
import sys
import pygame

from src.button import Button

from .constants import (
    BLACK,
    BLUE,
    DARK,
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
title_surf = title_font.render("PATHFINDER", True, DARK)


def main() -> None:
    """
    Start here
    """
    maze_list = [f"data/maze/{filename}"
                 for filename in os.listdir("data/maze")]
    maze_idx = 0
    maze_count = len(maze_list)

    maze = Maze(surface=WINDOW, filename=maze_list[maze_idx])
    button = Button(
        "START", WIDTH - 200, HEIGHT - 80,
        background_color=pygame.Color(*DARK),
        foreground_color=pygame.Color(*BLUE),
        padding=6, font_size=24, outline=True
    )
    button.rect.x -= button.rect.width

    algo_list = [
        Button(
            text="Breadth First Search",
            x=130,
            y=HEIGHT - 80,
            background_color=pygame.Color(*DARK),
            foreground_color=pygame.Color(*BLUE),
            padding=6, font_size=24, outline=True
        ),
        Button(
            text=" Depth First Search ",
            x=130,
            y=HEIGHT - 80,
            background_color=pygame.Color(*DARK),
            foreground_color=pygame.Color(*BLUE),
            padding=6, font_size=24, outline=True
        )
    ]
    algo_idx = 0
    algo_count = len(algo_list)
    algo_selector = algo_list[0]

    next_btn = Button(
        text=">",
        x=WIDTH - 40,
        y="center",
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
    )

    prev_btn = Button(
        text="<",
        x=5,
        y="center",
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
    )

    next_algo = Button(
        text=">",
        x=130 + algo_selector.rect.width + 5,
        y=(HEIGHT - 80) +
        (algo_selector.rect.height - next_btn.rect.height) / 2,
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
    )

    prev_algo = Button(
        text="<",
        x=125 - next_algo.rect.width,
        y=(HEIGHT - 80) +
        (algo_selector.rect.height - next_btn.rect.height) / 2,
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
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
            maze.solve(algo_list[algo_idx].text)
            pygame.time.delay(5000)

        if next_algo.draw(WINDOW):
            algo_idx += 1
            algo_idx %= algo_count
            pygame.time.delay(200)

        if prev_algo.draw(WINDOW):
            algo_idx -= 1
            algo_idx %= algo_count
            pygame.time.delay(200)

        algo_list[algo_idx].draw(WINDOW)

        if next_btn.draw(surf=WINDOW):
            maze_idx += 1
            maze_idx %= maze_count
            maze = Maze(surface=WINDOW, filename=maze_list[maze_idx])
            pygame.time.delay(200)

        if prev_btn.draw(surf=WINDOW):
            maze_idx -= 1
            maze_idx %= maze_count
            maze = Maze(surface=WINDOW, filename=maze_list[maze_idx])
            pygame.time.delay(200)

        pygame.display.update()
        CLOCK.tick(FPS)
