import sys
import pygame


from .animations import Animation, Animator, AnimatingNode
from .maze import GOAL, START, Maze, WEIGHT
from .widgets import Button, Label
from .constants import (
    BLUE,
    CELL_SIZE,
    CLOCK,
    DARK,
    DARK_BLUE,
    FONT_18,
    GRAY,
    GREEN,
    HEADER_HEIGHT,
    WHITE,
    WIDTH,
    HEIGHT,
    FPS,
    YELLOW
)

# Initialize PyGame
pygame.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWACCEL)
pygame.display.set_caption("Pathfinding Visualiser")

# Top bar
top = pygame.Rect(0, 0, WIDTH, 80)

# Title
title = Label(
    "Pathfinding Visualiser", 30, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, bold=True
)
title.rect.centery = top.centery

# Instantiate Maze and Animator
maze = Maze(surface=WINDOW)
animator = Animator(surface=WINDOW, maze=maze)
maze.animator = animator


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

# Button instance for VISUALISE button
visualise_btn = Button(
    "VISUALISE", "center", 0,
    background_color=pygame.Color(*GREEN),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False
)
visualise_btn.rect.centery = top.centery

#
generate_btn = Button(
    "Generate Maze", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False
)
generate_btn.rect.centery = top.centery
generate_btn.rect.left = visualise_btn.rect.right + 120

generating_options = [
    Button(
        text="Normal",
        x=generate_btn.rect.x + 20,
        y=generate_btn.rect.y + generate_btn.height,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=20, outline=False
    ),
    Button(
        text="Weighted",
        x=generate_btn.rect.x + 20,
        y=generate_btn.rect.y + generate_btn.height * 2,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=20, outline=False
    ),
]

# Button instance for Clear button
clear_btn = Button(
    "Clear Walls", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False
)
clear_btn.rect.centery = top.centery
clear_btn.rect.right = WIDTH - 30


def main() -> None:
    """Start here"""

    label = Label(
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
    algo_idx = -1

    show_generating_options = False
    generating_options_idx = -1

    visualising = False
    done_visualising = False
    generating = False
    draw_weighted_nodes = False

    dragging = False
    cell_under_mouse = (-1, -1)
    cell_value = ""

    while True:
        # Handle events
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
                    cell_under_mouse = (row, col)
                    cell_value = value

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_is_down = False
                animator.animating = False
                draw_weighted_nodes = False

                if dragging:
                    dragging = False

                    pos = pygame.mouse.get_pos()
                    if not maze.mouse_within_bounds(pos):
                        break

                    row, col = maze.get_cell_pos(pos)
                    if maze.get_cell_value((row, col)) in ("A", "B") or done_visualising:
                        break

                    maze.set_cell((row, col), cell_value)
                    maze.set_cell(cell_under_mouse, "1")

                cell_under_mouse = (-1, -1)

        if need_update:
            show_algorithms, need_update, visualising, show_generating_options, done_visualising = draw(
                label,
                algo_idx,
                visualising,
                done_visualising,
                show_generating_options,
                show_algorithms,
                need_update
            )

        # Get pressed keys for weighted nodes
        draw_weighted_nodes, key = get_pressed()

        # Draw walls | weighted nodes
        if mouse_is_down and not dragging and not visualising:
            pos = pygame.mouse.get_pos()

            if maze.mouse_within_bounds(pos):
                row, col = maze.get_cell_pos(pos)

                if cell_under_mouse != (row, col):
                    if maze.get_cell_value((row, col)) in ("1", "V", "*"):
                        rect = pygame.Rect(0, 0, 9, 9)
                        x, y = maze.coords[row][col]

                        if draw_weighted_nodes and key:

                            animator.add_nodes_to_animate([
                                AnimatingNode(
                                    rect=rect,
                                    center=(x + 15, y + 15),
                                    ticks=pygame.time.get_ticks(),
                                    value=str(key % 50 + 2),
                                    animation=Animation.WEIGHT_ANIMATION,
                                    color=WHITE,
                                    duration=50,
                                )
                            ])

                        else:
                            animator.add_nodes_to_animate([
                                AnimatingNode(
                                    rect=rect,
                                    center=(x + 15, y + 15),
                                    ticks=pygame.time.get_ticks(),
                                    value="#",
                                    color=DARK
                                )
                            ])

                    elif maze.get_cell_value((row, col)) not in ("A", "B"):
                        maze.set_cell((row, col), "1")

                    cell_under_mouse = (row, col)

        # Animate nodes
        if animator.nodes_to_animate:
            visualising = False
            show_generating_options = False
            animator.animating = True
            animator.animate_nodes()
        else:
            animator.animating = False

        # Handle moving start and target nodes
        if dragging and not done_visualising and not visualising:
            x, y = pygame.mouse.get_pos()
            if cell_value == "A":
                WINDOW.blit(START, (x - 10, y - 10))
            else:
                WINDOW.blit(GOAL, (x - 10, y - 10))

        # Instantly find path if dragging post visualisation
        if dragging and done_visualising and not visualising:
            x, y = pygame.mouse.get_pos()

            if maze.mouse_within_bounds((x, y)):
                row, col = maze.get_cell_pos((x, y))
                x, y = maze.coords[row][col]

                if cell_under_mouse != (row, col):
                    maze.set_cell((row, col), cell_value)
                    maze.set_cell(cell_under_mouse, "1")

                    instant_algorithm(maze, algo_list, algo_idx)
                    cell_under_mouse = (row, col)

        # Solve maze if visualise button is pressed and some
        # algorithm is selected
        if visualising and algo_idx > -1:
            maze.clear_visited()
            show_algorithms, need_update, visualising, show_generating_options, done_visualising = draw(
                label,
                algo_idx,
                visualising,
                done_visualising,
                show_generating_options,
                show_algorithms,
                need_update
            )
            maze.solve(algo_list[algo_idx].text)
            visualising = False
            done_visualising = True

        # Generate maze
        if generating:
            maze.generate_maze(weighted=generating_options_idx == 1)
            generating = False

        # Show algorithms list
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
            
            # Handle selection
            for btn in algo_list:
                if btn.draw(WINDOW):
                    show_algorithms = False
                    algo_idx = algo_list.index(btn)
                    label = Label(
                        btn.text, "center", 0,
                        background_color=pygame.Color(*WHITE),
                        foreground_color=pygame.Color(*DARK),
                        padding=6, font_size=20, outline=False
                    )
                    label.rect.bottom = HEADER_HEIGHT - 10

                    if done_visualising:
                        instant_algorithm(maze, algo_list, algo_idx)

        # Show maze generating options
        if show_generating_options:
            pygame.draw.rect(
                WINDOW,
                DARK_BLUE,
                (generate_btn.rect.x - 20,
                 generate_btn.rect.y + generate_btn.height,
                 generate_btn.width + 60,
                 generate_btn.height * len(generating_options) + 20),
                border_radius=10
            )

            # Handle selection
            for btn in generating_options:
                if btn.draw(WINDOW):
                    show_generating_options = False
                    generating_options_idx = generating_options.index(btn)
                    generating = True
                    maze.clear_board()

        # Update
        pygame.display.update()
        CLOCK.tick(FPS)


def instant_algorithm(maze: Maze, algo_list: list[Button], algo_idx: int):
    """Find path without animation

    Args:
        maze (_type_): Maze
        algo_list (_type_): Algorithm list
        algo_idx (_type_): Algorithm index
    """
    maze.clear_visited()

    solution = maze.solve(
        algo_list[algo_idx].text, visualize=False
    )

    path = solution.path
    explored = solution.explored

    # Mark explored nodes as blue
    for i, j in explored:
        if (i, j) in (maze.start, maze.goal):
            continue

        maze.set_cell((i, j), "V")

    # Mark optimal path nodes as yellow
    for i, j in path:
        if (i, j) in (maze.start, maze.goal):
            continue

        maze.set_cell((i, j), "*")


def get_pressed() -> tuple[bool, int | None]:
    """Return pressed key if number

    Returns:
        tuple[bool, int | None]: Whether a num key was pressed, 
                                 the key if found
    """
    keys = [pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    pressed = pygame.key.get_pressed()
    for key in keys:
        if pressed[key]:
            return True, key

    return False, None


def draw(
    label: Label,
    algo_idx: int,
    visualising: bool,
    done_visualising: bool,
    show_generating_options: bool,
    show_algorithms: bool,
    need_update: bool,
) -> tuple[bool, bool, bool, bool, bool]:
    """Draw things (except Visualise button)

    Args:
        label (Label): Selected algorithm label
        algo_idx (int): Index of selected algorithm
        visualising (bool): Whether to visualise
        done_visualisiing (bool): Whether visualisation is done
        show_generating_options (bool): Whether to show maze generation options
        show_algorithms (bool): Whether to show algorithms list
        need_update (bool): Whether to redraw content

    Returns:
        tuple[bool, bool, bool, bool, bool]: show_algorithms,
                                             need_update,
                                             visualising,
                                             show_generating_options,
                                             done_visualising
    """
    # Fill white, draw top background and title text
    WINDOW.fill(WHITE)
    pygame.draw.rect(WINDOW, DARK_BLUE, top)
    title.draw(WINDOW)

    # Draw maze legend
    texts = {
        "Start Node": WHITE,
        "Visited Node": BLUE,
        "Shortest-Path Node": YELLOW,
        "Unvisited Node": WHITE,
        "Wall Node": DARK,
        "Weighted Node": WHITE,
        "Target Node": WHITE,
    }

    x = 60
    y = top.bottom + 20
    for text in texts:
        # Rectangle (Symbol)
        pygame.draw.rect(WINDOW, texts[text], (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(
            WINDOW, GRAY, (x, y, CELL_SIZE, CELL_SIZE), width=1)

        # Text (Meaning)
        text_surf = FONT_18.render(text, True, DARK)
        text_rect = text_surf.get_rect()
        text_rect.centery = y + CELL_SIZE // 2

        WINDOW.blit(text_surf, (x + CELL_SIZE + 10, text_rect.y))

        # Formating
        if texts[text] == DARK:
            y += text_surf.get_height() + 20
        else:
            x += CELL_SIZE + 10 + text_surf.get_width() + 60

        # Draw images for weighted, start and target node
        if text == "Weighted Node":
            WINDOW.blit(WEIGHT, (x + 3, y + 3))
            x = 60
        elif text == "Start Node":
            image_rect = START.get_rect(center=(75, top.bottom + 35))
            WINDOW.blit(START, image_rect)
        elif text == "Target Node":
            image_rect = GOAL.get_rect(center=(75, y + 15))
            WINDOW.blit(GOAL, image_rect)

    # Draw algo label
    label.draw(WINDOW)

    # Handle buttons
    if algorithm_btn.draw(WINDOW) and not maze.animator.animating:
        show_algorithms = True

    if visualise_btn.draw(WINDOW) and algo_idx > -1 \
            and not maze.animator.animating:
        visualising = True

    if clear_btn.draw(WINDOW) and not maze.animator.animating:
        maze.clear_board()
        done_visualising = False
        need_update = True

    if generate_btn.draw(WINDOW) and not maze.animator.animating:
        show_generating_options = True

    maze.draw()

    return (
        show_algorithms,
        need_update,
        visualising,
        show_generating_options,
        done_visualising
    )
