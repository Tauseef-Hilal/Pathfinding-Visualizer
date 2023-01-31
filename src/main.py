import sys
import pygame


from .animations import Animation, Animator, AnimatingNode
from .maze import GOAL, START, Maze, WEIGHT
from .widgets import Button, Label, Menu
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
    PURPLE,
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
    x=title.width + 50,
    y=0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False
)
algorithm_btn.rect.centery = top.centery


algo_menu = Menu(
    button=algorithm_btn,
    children=[
        Button(
            text="A* Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            text="Dijkstra's Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            text="Greedy Best First Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 3,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            text="Breadth First Search",
            x=algorithm_btn.rect.x - 40,
            y=algorithm_btn.rect.y + algorithm_btn.height * 3,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
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
    button=speed_btn,
    children=[
        Button(
            text="Fast",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            text="Medium",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
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
    padding=6, font_size=20, outline=False
)
visualise_btn.rect.centery = top.centery

#
generate_btn = Button(
    "Generate Maze", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False
)
generate_btn.rect.centery = top.centery
generate_btn.rect.left = visualise_btn.rect.right + 120


generate_menu = Menu(
    button=generate_btn,
    children=[
        Button(
            text="Recursive Division",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            text="Random Maze",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            text="Basic Weight Maze",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            text="Recursive Division (Weighted)",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
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
    padding=6, font_size=20, outline=False
)
clear_btn.rect.centery = top.centery
clear_btn.rect.right = WIDTH - 20


def main() -> None:
    """Start here"""

    label = Label(
        "Choose an algorithm", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False
    )
    label.rect.bottom = HEADER_HEIGHT - 10

    speed_label = Label(
        text="Fast",
        font_size=16,
        x=speed_btn.rect.x,
        y=speed_btn.rect.bottom,
        foreground_color=pygame.Color(*WHITE),
        background_color=pygame.Color(*PURPLE),
    )
    speed_label.rect.centerx = speed_btn.rect.centerx

    # Game loop
    mouse_is_down = False
    need_update = True

    done_visualising = False
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
            label, speed_label, done_visualising, need_update = draw(
                label,
                speed_label,
                done_visualising,
                need_update
            )

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
            animator.animating = True
            animator.animate_nodes()
        else:
            animator.animating = False

        # Handle moving start and target nodes
        if dragging and not done_visualising and not animator.animating:
            x, y = pygame.mouse.get_pos()
            if cell_value == "A":
                WINDOW.blit(START, (x - 10, y - 10))
            else:
                WINDOW.blit(GOAL, (x - 10, y - 10))

        # Instantly find path if dragging post visualisation
        if dragging and done_visualising and not animator.animating:
            x, y = pygame.mouse.get_pos()

            if maze.mouse_within_bounds((x, y)):
                row, col = maze.get_cell_pos((x, y))
                x, y = maze.coords[row][col]

                if cell_under_mouse != (row, col):
                    maze.set_cell((row, col), cell_value)
                    maze.set_cell(cell_under_mouse, "1")

                    text = label.text.split(" takes")[0]
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
    
    solution = maze.solve(
        algo_name=algo_name, visualize=False
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
    speed_label: Label,
    done_visualising: bool,
    need_update: bool,
) -> tuple[Label, Label, bool, bool]:
    """Draw things (except Visualise button)

    Args:
        label (Label): Selected algorithm label
        done_visualisiing (bool): Whether visualisation is done
        need_update (bool): Whether to redraw content

    Returns:
        tuple[Label, Label, bool, bool]: label, speed_label, done_visualising, need_update,
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
            y += text_surf.get_height() + 30
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
    speed_label.draw(WINDOW)

    maze.draw()

    # Handle buttons
    if (algo_menu.draw(WINDOW) or algo_menu.clicked) \
            and not maze.animator.animating:
        if algo_menu.selected:
            label = Label(
                algo_menu.selected.text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False
            )
            label.rect.bottom = HEADER_HEIGHT - 10

            if done_visualising:
                text = label.text.split(" takes")[0]
                instant_algorithm(maze, text)

    if (speed_menu.draw(WINDOW) or speed_menu.clicked) \
            and not maze.animator.animating:
        if speed_menu.selected:
            speed_label = Label(
                text=speed_menu.selected.text,
                font_size=16,
                x=speed_btn.rect.x,
                y=speed_btn.rect.bottom,
                foreground_color=pygame.Color(*WHITE),
                background_color=pygame.Color(*PURPLE),
            )
            speed_label.rect.centerx = speed_btn.rect.centerx
            maze.set_speed(speed_menu.selected.text)

    if visualise_btn.draw(WINDOW) and not label.text.startswith("Choose") \
            and not maze.animator.animating:
        maze.clear_visited()

        text = label.text.split(" takes")[0]
        solution = maze.solve(text)
        steps = len(solution.explored)
        time_taken = solution.time
        label = Label(
            text  + f" takes {steps} steps in {time_taken:.2f}ms", "center", 0,
            background_color=pygame.Color(*WHITE),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=20, outline=False
        )
        label.rect.bottom = HEADER_HEIGHT - 10
        done_visualising = True

    if clear_btn.draw(WINDOW) and not maze.animator.animating:
        maze.clear_board()
        done_visualising = False
        need_update = True

    if (generate_menu.draw(WINDOW) or generate_menu.clicked) \
            and not animator.animating:
        if generate_menu.selected:
            maze.clear_board()
            maze.generate_maze(
                algorithm=generate_menu.selected.text,
                weighted="Weighted" in generate_menu.selected.text
            )

    return (
        label,
        speed_label,
        done_visualising,
        need_update,
    )
