import os
import sys
import pygame

from .maze import Maze
from .button import Button
from .constants import (
    BLUE,
    DARK,
    WHITE,
    WIDTH,
    HEIGHT,
    FPS
)

# Initialize PyGame
pygame.init()
pygame.font.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder")

# Set up clock
CLOCK = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Verdana", 40, True)
title_surf = title_font.render("PATHFINDER", True, DARK)


def main() -> None:
    """Start here"""

    # Load maze file paths
    maze_list = [f"data/maze/{filename}"
                 for filename in os.listdir("data/maze")]

    maze_count = len(maze_list)

    # Instantiate Maze with first file
    maze_idx = 0
    maze = Maze(surface=WINDOW, filename=maze_list[maze_idx])

    # Buttons for switching between mazes
    next_maze = Button(
        text=">",
        x=WIDTH - 40,
        y="center",
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
    )

    prev_maze = Button(
        text="<",
        x=5,
        y="center",
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
    )

    # Algorithms list
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
        ),
        # Button(
        #     text="     A*  Search     ",
        #     x=130,
        #     y=HEIGHT - 80,
        #     background_color=pygame.Color(*DARK),
        #     foreground_color=pygame.Color(*BLUE),
        #     padding=6, font_size=24, outline=True
        # )
    ]

    algo_idx = 0
    algo_count = len(algo_list)

    # Buttons for switching between algorithms
    next_algo = Button(
        text=">",
        x=130 + algo_list[0].rect.width + 5,
        y=(HEIGHT - 80) + (algo_list[0].rect.height - 47) / 2,
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
    )

    prev_algo = Button(
        text="<",
        x=125 - next_algo.rect.width,
        y=(HEIGHT - 80) + (algo_list[0].rect.height - 47) / 2,
        font_size=30,
        bold=True,
        background_color=pygame.Color(*WHITE)
    )

    # Button instance for START button
    button = Button(
        "START", WIDTH - 200, HEIGHT - 80,
        background_color=pygame.Color(*DARK),
        foreground_color=pygame.Color(*BLUE),
        padding=6, font_size=24, outline=True
    )

    button.rect.x -= button.rect.width

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw title text
        WINDOW.fill(WHITE)
        WINDOW.blit(title_surf, ((WIDTH - title_surf.get_width()) / 2, 20))

        # Draw maze and its buttons
        maze.draw()

        if next_maze.draw(surf=WINDOW):
            maze_idx += 1
            maze_idx %= maze_count
            maze = Maze(surface=WINDOW, filename=maze_list[maze_idx])
            pygame.time.delay(200)

        if prev_maze.draw(surf=WINDOW):
            maze_idx -= 1
            maze_idx %= maze_count
            maze = Maze(surface=WINDOW, filename=maze_list[maze_idx])
            pygame.time.delay(200)

        # Draw buttons for switching algorithms
        algo_list[algo_idx].draw(WINDOW)

        if next_algo.draw(WINDOW):
            algo_idx += 1
            algo_idx %= algo_count
            pygame.time.delay(200)

        if prev_algo.draw(WINDOW):
            algo_idx -= 1
            algo_idx %= algo_count
            pygame.time.delay(200)

        # Draw START button
        if button.draw(WINDOW):
            maze.solve(algo_list[algo_idx].text)
            pygame.time.delay(5000)

        # Update
        pygame.display.update()
        CLOCK.tick(FPS)
