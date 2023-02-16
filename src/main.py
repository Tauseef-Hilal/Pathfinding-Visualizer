import sys
import pygame

from .state import State
from .generate import MazeGenerator
from .animations import Animation, Animator, AnimatingNode
from .maze import GOAL, START, Maze, WEIGHT

from .widgets import (
    Alignment,
    Button,
    Label,
    Menu,
    Orientation,
    Popup,
    Table,
    TableCell
)

from .constants import (
    BLUE,
    CELL_SIZE,
    CLOCK,
    DARK,
    DARK_BLUE,
    FONT_18,
    GRAY,
    GREEN,
    GREEN_2,
    HEADER_HEIGHT,
    BLUE_2,
    MIN_SIZE,
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
    "Pathfinding Visualiser", 20, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, bold=True,
    surface=WINDOW,
)
title.rect.centery = top.centery

# Instantiate Maze and Animator
state = State()
maze = Maze(surface=WINDOW)
animator = Animator(surface=WINDOW, maze=maze)
maze_generator = MazeGenerator(animator=animator)
maze.animator = animator
maze.generator = maze_generator


# Algorithms list
algorithm_btn = Button(
    surface=WINDOW,
    text="Algorithms",
    x=title.width + 70,
    y=0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False
)
algorithm_btn.rect.centery = top.centery


algo_menu = Menu(
    surface=WINDOW,
    button=algorithm_btn,
    children=[
        Button(
            surface=WINDOW,
            text="A* Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Dijkstra's Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Greedy Best First Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 3,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Breadth First Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 3,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Depth First Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 4,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)

speed_btn = Button(
    surface=WINDOW,
    text="Speed",
    x=algorithm_btn.rect.right + 40,
    y=0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False
)
speed_btn.rect.centery = top.centery
speed_btn.rect.y -= 15


speed_menu = Menu(
    surface=WINDOW,
    button=speed_btn,
    children=[
        Button(
            surface=WINDOW,
            text="Fast",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Medium",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Slow",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)

# Button instance for VISUALISE button
visualise_btn = Button(
    "VISUALISE", "center", 0,
    background_color=pygame.Color(*GREEN),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False,
    surface=WINDOW,
)
visualise_btn.rect.centery = top.centery

#
compare_btn = Button(
    "Run All    ", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False,
    surface=WINDOW,
)
compare_btn.rect.centery = top.centery
compare_btn.rect.left = visualise_btn.rect.right + 50

comapre_menu = Menu(
    surface=WINDOW,
    button=compare_btn,
    children=[
        Button(
            surface=WINDOW,
            text="Current Maze",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Different Mazes",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)

generate_btn = Button(
    "Generate Maze", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False,
    surface=WINDOW,
)
generate_btn.rect.centery = top.centery
generate_btn.rect.left = compare_btn.rect.right + 50


generate_menu = Menu(
    surface=WINDOW,
    button=generate_btn,
    children=[
        Button(
            surface=WINDOW,
            text="Recursive Division",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),

        Button(
            surface=WINDOW,
            text="Prim's Algorithm",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Randomised DFS",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Basic Random Maze",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=WINDOW,
            text="Basic Weight Maze",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)


# Button instance for Clear button
clear_btn = Button(
    "Clear Walls", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False,
    surface=WINDOW,
)
clear_btn.rect.centery = top.centery
clear_btn.rect.right = WIDTH - 20


def main() -> None:
    """Start here"""
    state.label = Label(
        "Choose an algorithm", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=WINDOW,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 10

    state.speed_label = Label(
        surface=WINDOW,
        text="Fast",
        font_size=16,
        x=speed_btn.rect.x,
        y=speed_btn.rect.bottom,
        foreground_color=pygame.Color(*WHITE),
        background_color=pygame.Color(*BLUE_2),
    )
    state.speed_label.rect.centerx = speed_btn.rect.centerx

    # Game loop
    mouse_is_down = False
    state.done_visualising = False
    state.need_update = True

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
                if state.overlay:
                    break

                state.need_update = True
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
                    if maze.get_cell_value((row, col)) in ("A", "B") or state.done_visualising:
                        break

                    maze.set_cell((row, col), cell_value)
                    maze.set_cell(cell_under_mouse, "1")

                cell_under_mouse = (-1, -1)

        if state.need_update:
            draw()

        # Get pressed keys for weighted nodes
        draw_weighted_nodes, key = get_pressed()

        # Draw walls | weighted nodes
        # This should not run when animating solution
        if mouse_is_down and not dragging:
            pos = pygame.mouse.get_pos()

            if maze.mouse_within_bounds(pos):
                row, col = maze.get_cell_pos(pos)

                if cell_under_mouse != (row, col):
                    if maze.get_cell_value((row, col)) in ("1", "V", "*"):
                        rect = pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE)
                        x, y = maze.coords[row][col]

                        if draw_weighted_nodes and key:

                            animator.add_nodes_to_animate([
                                AnimatingNode(
                                    rect=rect,
                                    center=(x + CELL_SIZE // 2,
                                            y + CELL_SIZE // 2),
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
                                    center=(x + CELL_SIZE // 2,
                                            y + CELL_SIZE // 2),
                                    ticks=pygame.time.get_ticks(),
                                    value="#",
                                    color=DARK
                                )
                            ])

                    elif maze.get_cell_value((row, col)) not in ("A", "B"):
                        maze.set_cell((row, col), "1")

                    cell_under_mouse = (row, col)

        # Animate nodes
        if animator.nodes_to_animate and state.need_update:
            animator.animating = True
            animator.animate_nodes()
        else:
            animator.animating = False

        # Handle moving start and target nodes
        if dragging and not state.done_visualising and not animator.animating:
            x, y = pygame.mouse.get_pos()
            if cell_value == "A":
                WINDOW.blit(START, (x - 10, y - 10))
            else:
                WINDOW.blit(GOAL, (x - 10, y - 10))

        # Instantly find path if dragging post visualisation
        if dragging and state.done_visualising and not animator.animating:
            x, y = pygame.mouse.get_pos()

            if maze.mouse_within_bounds((x, y)):
                row, col = maze.get_cell_pos((x, y))
                x, y = maze.coords[row][col]

                if cell_under_mouse != (row, col):
                    maze.set_cell((row, col), cell_value)
                    maze.set_cell(cell_under_mouse, "1")

                    text = state.label.text.split(" took")[0]
                    instant_algorithm(maze, text)
                    cell_under_mouse = (row, col)

        # Update
        pygame.display.update()
        CLOCK.tick(FPS)


def instant_algorithm(maze: Maze, algo_name: str):
    """Find path without animation

    Args:
        maze (Maze): Maze
        algo_name (str): Algorithm name
    """
    maze.clear_visited()

    solution = maze.solve(algo_name=algo_name)

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


def draw() -> None:
    """Draw things (except Visualise button)
    """
    # Fill white, draw top background and title text
    WINDOW.fill(WHITE)
    pygame.draw.rect(WINDOW, DARK_BLUE, top)
    title.draw()

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

    x = 50
    y = top.bottom + 20
    for text in texts:
        # Rectangle (Symbol)
        pygame.draw.rect(WINDOW, texts[text], (x, y, 30, 30))
        pygame.draw.rect(WINDOW, GRAY, (x, y, 30, 30), width=1)

        # Text (Meaning)
        text_surf = FONT_18.render(text, True, DARK)
        text_rect = text_surf.get_rect()
        text_rect.centery = y + 30 // 2

        WINDOW.blit(text_surf, (x + 30 + 10, text_rect.y))

        # Formating
        if texts[text] == DARK:
            y += text_surf.get_height() + 30
        elif text != "Weighted Node":
            x += 30 + 10 + text_surf.get_width() + 75

        # Draw images for weighted, start and target node
        if text == "Weighted Node":
            WINDOW.blit(WEIGHT, (x + 3, y + 3))
            x = 50
        elif text == "Start Node":
            image_rect = START.get_rect(center=(65, top.bottom + 35))
            WINDOW.blit(START, image_rect)
        elif text == "Target Node":
            image_rect = GOAL.get_rect(center=(65, y + 15))
            WINDOW.blit(GOAL, image_rect)

    # Draw algo label
    state.label.draw()
    state.speed_label.draw()

    maze.draw()

    # Handle buttons
    if (algo_menu.draw() or algo_menu.clicked) \
            and not maze.animator.animating:
        state.overlay = True
        if algo_menu.selected:
            state.label = Label(
                algo_menu.selected.text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            )
            state.label.rect.bottom = HEADER_HEIGHT - 10

            if state.done_visualising:
                text = state.label.text.split(" takes")[0]
                instant_algorithm(maze, text)

            state.overlay = False

    if (speed_menu.draw() or speed_menu.clicked) \
            and not maze.animator.animating:
        state.overlay = True

        if speed_menu.selected:
            state.speed_label = Label(
                surface=WINDOW,
                text=speed_menu.selected.text,
                font_size=16,
                x=speed_btn.rect.x,
                y=speed_btn.rect.bottom,
                foreground_color=pygame.Color(*WHITE),
                background_color=pygame.Color(*BLUE_2),
            )
            state.speed_label.rect.centerx = speed_btn.rect.centerx
            maze.set_speed(speed_menu.selected.text)
            state.overlay = False

    if visualise_btn.draw() \
        and not state.label.text.startswith("Choose") \
            and not maze.animator.animating:
        state.overlay = True

        text = state.label.text.split(" took")[0]
        text = text.split("Running ")[-1]
        idx = [algo_menu.children.index(btn)
               for btn in algo_menu.children if btn.text == text][0]
        run_single(idx)

    if clear_btn.draw() and not maze.animator.animating:
        maze.clear_board()
        state.done_visualising = False
        state.need_update = True

    if (comapre_menu.draw() or comapre_menu.clicked) \
            and not animator.animating:
        state.overlay = True

        if comapre_menu.selected \
                and comapre_menu.selected.text == "Current Maze":
            state.results = {}
            run_all(0)
        elif comapre_menu.selected \
                and comapre_menu.selected.text == "Different Mazes":
            state.run_all_mazes = True
            state.results = {}
            run_all(0)

    if (generate_menu.draw() or generate_menu.clicked) \
            and not animator.animating:
        state.overlay = True

        if generate_menu.selected:
            maze.clear_board()
            text = state.label.text

            def callback():
                state.overlay = False
                state.label = Label(
                    f"{text}", "center", 0,
                    background_color=pygame.Color(*WHITE),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=WINDOW,
                )
                state.label.rect.bottom = HEADER_HEIGHT - 10

            maze.generate_maze(
                algorithm=generate_menu.selected.text,
                after_generation=callback
            )

            algorithm = generate_menu.selected.text

            if "Weight" in algorithm:
                new_text = "Generating basic weight maze"
            elif "Basic Random" in algorithm:
                new_text = "Generating maze randomly"
            else:
                new_text = f"Generating maze using {algorithm}"

            state.label = Label(
                new_text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            )
            state.label.rect.bottom = HEADER_HEIGHT - 10

    if state.results_popup:
        state.overlay = True
        if state.results_popup.draw():
            state.results_popup = None
            state.overlay = False


def run_single(idx: int) -> None:
    """Run a single algorithm on one maze

    Args:
        idx (int): Algorithm index
    """
    maze.clear_visited()
    text = algo_menu.children[idx].text
    solution = maze.solve(text)

    def callback():
        state.done_visualising = True
        state.label = Label(
            f"{text} took {solution.explored_length} steps in "
            f"{solution.time:.2f}ms", "center", 0,
            background_color=pygame.Color(*WHITE),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=20, outline=False,
            surface=WINDOW,
        )
        state.label.rect.bottom = HEADER_HEIGHT - 10
        state.overlay = False

    maze.visualize(solution=solution, after_animation=callback)

    state.label = Label(
        f"Running {text}", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=WINDOW,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 10


def run_all(algo_idx: int, maze_idx: int = -1) -> None:
    """Run all the algorithms on current or all mazes

    Args:
        algo_idx (int): Algorithm index
        maze_idx (int, optional): Maze index. Defaults to -1.
    """
    maze.clear_visited()
    text = algo_menu.children[algo_idx].text

    def callback():
        if algo_idx + 1 < len(algo_menu.children):
            run_all(algo_idx + 1, maze_idx)
        elif state.run_all_mazes \
                and maze_idx + 1 < len(generate_menu.children):
            maze.clear_board()

            def after_generation():
                run_all(0, maze_idx + 1)

            maze.generate_maze(
                algorithm=generate_menu.children[maze_idx + 1].text,
                after_generation=after_generation
            )

            algorithm = generate_menu.children[maze_idx + 1].text

            if "Weight" in algorithm:
                new_text = "Generating basic weight maze"
            elif "Basic Random" in algorithm:
                new_text = "Generating maze randomly"
            else:
                new_text = f"Generating maze using {algorithm}"

            state.label = Label(
                new_text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            )
            state.label.rect.bottom = HEADER_HEIGHT - 10
        else:
            state.label = Label(
                text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            )
            state.label.rect.bottom = HEADER_HEIGHT - 10

            results = list(state.results.items())

            if state.run_all_mazes:
                for result in results:
                    result[1]["path_length"] //= maze_idx + 2
                    result[1]["path_cost"] //= maze_idx + 2
                    result[1]["explored_length"] //= maze_idx + 2
                    result[1]["time"] /= maze_idx + 2

            results.sort(key=lambda item: item[1]["time"])

            show_results(results)
            state.run_all_mazes = False
            state.overlay = False

    solution = maze.solve(text)

    if text not in state.results:
        state.results[text] = vars(solution)
    else:
        state.results[text]["explored_length"] += solution.explored_length
        state.results[text]["path_length"] += solution.path_length
        state.results[text]["path_cost"] += solution.path_cost
        state.results[text]["time"] += solution.time

    maze.visualize(solution=solution, after_animation=callback)

    state.label = Label(
        f"Running {text}", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=WINDOW,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 10


def show_results(results: list[tuple[str, dict[str, float]]]) -> None:
    """Display results

    Args:
        results (list[tuple[str, dict[str, float]]]): Result data
    """
    children: list[list[TableCell]] = []
    children.append([
        TableCell(
            child=Label(
                    "Algorithm", 0, 0,
                    background_color=pygame.Color(*DARK_BLUE),
                    foreground_color=pygame.Color(*WHITE),
                    padding=6, font_size=20, outline=False,
                    surface=WINDOW,
                    ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Steps Explored", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Path Length", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Path Cost", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Time Taken", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
    ])

    colors = [GREEN_2, GREEN_2, YELLOW, YELLOW]
    colors.extend([GRAY] * (len(results) - 4))

    for i, result in enumerate(results):
        children.append([
            TableCell(
                child=Label(
                        f"{i + 1}. {result[0]}", 0, 0,
                        background_color=pygame.Color(*colors[i]),
                        foreground_color=pygame.Color(*DARK),
                        padding=6, font_size=20, outline=False,
                        surface=WINDOW,
                        ),
                color=colors[i],
                align=Alignment.LEFT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['explored_length']}", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=WINDOW,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['path_length']}", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=WINDOW,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['path_cost']}", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=WINDOW,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['time']:.2f}ms", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=WINDOW,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
        ])

    popup = Popup(
        WINDOW,
        0,
        0,
        padding=20,
        color=DARK,
        orientation=Orientation.VERTICAL,
        x_align=Alignment.CENTER,
        y_align=Alignment.CENTER,
        children=[
            Label(
                "COMPARISON RESULTS", 0, 0,
                background_color=pygame.Color(*DARK),
                foreground_color=pygame.Color(*WHITE),
                padding=10, font_size=20, outline=False,
                surface=WINDOW,
            ),
            Table(
                x=0,
                y=0,
                rows=6,
                columns=5,
                padding=20,
                color=DARK,
                children=children,
            )
        ],
    )

    popup.update_center(WINDOW.get_rect().center)
    popup.set_surface(WINDOW)
    state.results_popup = popup
