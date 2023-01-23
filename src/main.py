import sys
import pygame

from .maze import Maze
from .button import Button
from .constants import (
    BLUE,
    CELL_SIZE,
    DARK,
    DARK_BLUE,
    GREEN,
    HEADER_HEIGHT,
    MAZE_HEIGHT,
    RED,
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


def main() -> None:
    """Start here"""
    top = pygame.Rect(0, 0, WIDTH, 80)

    # Title
    title = Button(
        "Pathfinding Visualiser", 30, 0,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=20, bold=True
    )
    title.rect.centery = top.centery

    # Instantiate Maze
    maze = Maze(surface=WINDOW)

    # Algorithms list
    algorithm_btn = Button(
        text="Algorithms",
        x=title.width + 100,
        y=0,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=20, outline=False
    )
    algorithm_btn.rect.centery = top.centery

    algo_list = [
        Button(
            text="Breadth First Search",
            x=algorithm_btn.rect.x,
            y=algorithm_btn.rect.y + algorithm_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=20, outline=False
        ),
        Button(
            text="Depth First Search",
            x=algorithm_btn.rect.x,
            y=algorithm_btn.rect.y + algorithm_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=20, outline=False
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

    algo_idx = -1

    # Button instance for VISUALISE button
    button = Button(
        "VISUALISE", "center", 0,
        background_color=pygame.Color(*GREEN),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=20, outline=False
    )
    button.rect.centery = top.centery

    # Button instance for Clear button
    clear_btn = Button(
        "Clear Walls", 0, 0,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=20, outline=False
    )
    clear_btn.rect.centery = top.centery
    clear_btn.rect.right = WIDTH - 30

    label = Button(
        "Choose an algorithm", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False
    )
    label.rect.bottom = HEADER_HEIGHT - 10

    # Game loop
    mouse_is_down = False
    need_update = True
    show_algorithms = False
    visualising = False

    dragging = False
    dragged_cell = (0, 0)
    dragged_cell_value = "A"
    cell_under_mouse = (-1, -1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                need_update = True
                pos = pygame.mouse.get_pos()

                if not maze.mouse_within_bounds(pos):
                    break

                mouse_is_down = True

                row, col = maze.get_cell_pos(pos)
                if (value := maze.get_cell_value((row, col))) in ("A", "B"):
                    dragging = True
                    dragged_cell = row, col
                    dragged_cell_value = value

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_is_down = False
                cell_under_mouse = (-1, -1)

                if dragging:
                    dragging = False

                    pos = pygame.mouse.get_pos()
                    if not maze.mouse_within_bounds(pos):
                        break

                    row, col = maze.get_cell_pos(pos)
                    if maze.get_cell_value((row, col)) != " ":
                        break

                    maze.set_cell(dragged_cell, " ")
                    maze.set_cell((row, col), dragged_cell_value)

                    if dragged_cell_value == "A":
                        maze.update_ends(start=dragged_cell)
                    else:
                        maze.update_ends(goal=dragged_cell)

        if need_update:
            show_algorithms, need_update, visualising = draw(
                maze, top, title, algorithm_btn, button,
                visualising, clear_btn, show_algorithms, need_update
            )

        if mouse_is_down and not dragging:
            pos = pygame.mouse.get_pos()
            if maze.mouse_within_bounds(pos):
                row, col = maze.get_cell_pos(pos)

                if cell_under_mouse != (row, col):
                    if maze.get_cell_value((row, col)) == " ":
                        maze.set_cell((row, col), "#")
                    else:
                        maze.set_cell((row, col), " ")

                    cell_under_mouse = (row, col)

        if dragging:
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(
                WINDOW,
                RED if dragged_cell_value == "A" else GREEN,
                (x - 10, y - 10, 20, 20)
            )

        if show_algorithms:
            pygame.draw.rect(
                WINDOW,
                DARK_BLUE,
                (algorithm_btn.rect.x,
                 algorithm_btn.rect.y + algorithm_btn.height,
                 algorithm_btn.width * 2,
                 algorithm_btn.height * len(algo_list) + 20)
            )

            for btn in algo_list:
                if btn.draw(WINDOW):
                    show_algorithms = False
                    algo_idx = algo_list.index(btn)
                    label = Button(
                        btn.text, "center", 0,
                        background_color=pygame.Color(*WHITE),
                        foreground_color=pygame.Color(*DARK),
                        padding=6, font_size=20, outline=False
                    )
                    label.rect.bottom = HEADER_HEIGHT - 10
        label.draw(WINDOW)

        if visualising and (algo_idx > -1):
            show_algorithms, need_update, visualising = draw(
                maze, top, title, algorithm_btn, button,
                visualising, clear_btn, show_algorithms, need_update
            )
            maze.solve(algo_list[algo_idx].text)
            need_update = False
            visualising = False

        # Update
        pygame.display.update()
        CLOCK.tick(FPS)


def draw(
    maze: Maze,
    top: pygame.Rect,
    title: Button,
    algorithm_btn: Button,
    visualise_btn: Button,
    visualising: bool,
    clear_btn: Button,
    show_algorithms: bool,
    need_update: bool
) -> tuple[bool, bool, bool]:
    """Draw things (except Visualise button)

    Args:
        maze (Maze): Maze object
        top (pygame.Rect): Rect object
        title (Button): Title
        algorithm_btn (Button): Algorithms switcher button
        visualise_btn (Button): Visualise button
        visualising (bool): Whether to visualise
        clear_btn (Button): Clear walls button
        show_algorithms (bool): Whether to show algorithms list
        need_update (bool): Whether to redraw content

    Returns:
        tuple[bool, bool]: show_algorithms, need_update
    """
    WINDOW.fill(WHITE)
    pygame.draw.rect(WINDOW, DARK_BLUE, top)
    title.draw(WINDOW)

    if algorithm_btn.draw(WINDOW):
        show_algorithms = True
    
    if visualise_btn.draw(WINDOW):
        visualising = True

    if clear_btn.draw(WINDOW):
        maze.clear_walls()
        need_update = True

    maze.draw()
    return show_algorithms, need_update, visualising
