import sys
import pygame

from .maze import Maze, weight
from .button import Button
from .constants import (
    BLUE,
    CELL_SIZE,
    DARK,
    DARK_BLUE,
    GRAY,
    GREEN,
    HEADER_HEIGHT,
    WHITE_2,
    RED,
    WHITE,
    WIDTH,
    HEIGHT,
    FPS,
    YELLOW
)

# Initialize PyGame
pygame.init()
pygame.font.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder")

# Set up clock
CLOCK = pygame.time.Clock()

# Font
FONT = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 18)


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
            text="A* Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=20, outline=False
        ),
        Button(
            text="Dijkstra's Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=20, outline=False
        ),
        Button(
            text="Breadth First Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 3,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=20, outline=False
        ),
        Button(
            text="Depth First Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 4,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=20, outline=False
        ),
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

    #
    generate = Button(
        "Generate Maze", 0, 0,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=20, outline=False
    )
    generate.rect.centery = top.centery
    generate.rect.left = button.rect.right + 120

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
    generating = False
    draw_weighted_nodes = False

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
                draw_weighted_nodes = False
                cell_under_mouse = (-1, -1)

                if dragging:
                    dragging = False

                    pos = pygame.mouse.get_pos()
                    if not maze.mouse_within_bounds(pos):
                        break

                    row, col = maze.get_cell_pos(pos)
                    maze.set_cell(dragged_cell, " ", forced=True)

                    if dragged_cell_value == "A":
                        maze.update_ends(start=(row, col))
                    else:
                        maze.update_ends(goal=(row, col))

        if need_update:
            show_algorithms, need_update, visualising, generating = draw(
                maze, top, title, algorithm_btn, algo_idx, button,
                visualising, generate, generating, clear_btn, label, show_algorithms, need_update
            )

        draw_weighted_nodes = pygame.key.get_pressed()[pygame.K_w]

        if mouse_is_down and not dragging:
            pos = pygame.mouse.get_pos()
            if maze.mouse_within_bounds(pos):
                row, col = maze.get_cell_pos(pos)

                if cell_under_mouse != (row, col):
                    if maze.get_cell_value((row, col)) in (" ", "V", "*"):
                        maze.set_cell(
                            (row, col), "#" if not draw_weighted_nodes else "W"
                        )
                    elif maze.get_cell_value((row, col)) not in ("A", "B"):
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
                (algorithm_btn.rect.x - 50,
                 algorithm_btn.rect.y + algorithm_btn.height,
                 algorithm_btn.width * 2,
                 algorithm_btn.height * len(algo_list) + 20),
                border_radius=10
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

        if visualising and algo_idx > -1:
            maze.clear_visited()
            show_algorithms, need_update, visualising, generating = draw(
                maze, top, title, algorithm_btn, algo_idx, button,
                visualising, generate, generating, clear_btn, label, show_algorithms, need_update
            )
            maze.solve(algo_list[algo_idx].text)
            need_update = False
            visualising = False

        if generating:
            maze.generate_maze()
            generating = False

        # Update
        pygame.display.update()
        CLOCK.tick(FPS)


def draw(
    maze: Maze,
    top: pygame.Rect,
    title: Button,
    algorithm_btn: Button,
    algo_idx: int,
    visualise_btn: Button,
    visualising: bool,
    generate_btn: Button,
    generating: bool,
    clear_btn: Button,
    label: Button,
    show_algorithms: bool,
    need_update: bool
) -> tuple[bool, bool, bool, bool]:
    """Draw things (except Visualise button)

    Args:
        maze (Maze): Maze object
        top (pygame.Rect): Rect object
        title (Button): Title
        algorithm_btn (Button): Algorithms switcher button
        algo_idx (int): Index of selected algorithm
        visualise_btn (Button): Visualise button
        visualising (bool): Whether to visualise
        generate_btn (Button): Generate maze button
        clear_btn (Button): Clear walls button
        label (Button): Label
        show_algorithms (bool): Whether to show algorithms list
        need_update (bool): Whether to redraw content

    Returns:
        tuple[bool, bool]: show_algorithms, need_update, visualising, generating
    """
    WINDOW.fill(WHITE)
    pygame.draw.rect(WINDOW, DARK_BLUE, top)
    title.draw(WINDOW)

    if algorithm_btn.draw(WINDOW):
        show_algorithms = True

    if visualise_btn.draw(WINDOW) and algo_idx > -1:
        visualising = True

    if clear_btn.draw(WINDOW):
        maze.clear_walls()
        need_update = True

    if generate_btn.draw(WINDOW):
        maze.clear_walls()
        need_update = True
        generating = True

    texts = {
        "Start Node": RED,
        "Unvisited Node": WHITE,
        "Visited Node": BLUE,
        "Shortest-Path Node": YELLOW,
        "Wall Node": DARK,
        "Weighted Node": WHITE_2,
        "Target Node": GREEN,
    }

    x = 60
    y = top.bottom + 20
    for text in texts:
        pygame.draw.rect(WINDOW, texts[text], (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(
            WINDOW, GRAY, (x, y, CELL_SIZE, CELL_SIZE), width=1)
        
        text_surf = FONT.render(text, True, DARK)
        text_rect = text_surf.get_rect()
        text_rect.centery = y + CELL_SIZE // 2

        WINDOW.blit(text_surf, (x + CELL_SIZE + 10, text_rect.y))
        
        if texts[text] == WHITE_2:
            WINDOW.blit(weight, (x + 3, y + 3))
            x = 60

        elif texts[text] == DARK:
            y += text_surf.get_height() + 20
        else:
            x += CELL_SIZE + 10 + text_surf.get_width() + 60


    label.draw(WINDOW)

    maze.draw()
    return show_algorithms, need_update, visualising, generating
