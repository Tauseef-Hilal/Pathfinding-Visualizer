import random
import pygame

from .button import Button
from .animations import AnimatingNode, Animator
from .pathfinder.models.node import Node
from .pathfinder.models.solution import Solution
from .pathfinder.main import PathFinder
from .pathfinder.models.grid import Grid
from .pathfinder.models.search_types import Search

from .constants import (
    CELL_SIZE,
    DARK_BLUE,
    GRAY,
    MAZE_HEIGHT,
    HEADER_HEIGHT,
    MAZE_WIDTH,
    WIDTH,
    BLUE,
    DARK,
    WHITE,
    GREEN,
    RED,
    YELLOW
)

pygame.font.init()

WEIGHT = pygame.image.load("assets/images/weight.png")
FONT = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 14)


class Maze:
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface
        self.animator: Animator

        self.width = MAZE_WIDTH // CELL_SIZE
        self.height = MAZE_HEIGHT // CELL_SIZE

        self.maze = [[Node("1", (rowIdx, colIdx), 1)
                      for colIdx in range(self.width)]
                     for rowIdx in range(self.height)]

        self.start = (self.height // 2, 10)
        self.maze[self.start[0]][self.start[1]].value = "A"
        self.maze[self.start[0]][self.start[1]].cost = 0

        self.goal = (self.height // 2, self.width - 11)
        self.maze[self.goal[0]][self.goal[1]].value = "B"
        self.maze[self.goal[0]][self.goal[1]].cost = 1

        # Generate screen coordinates for maze
        self.coords = self._generate_coordinates()

    def _generate_coordinates(self) -> list[list[tuple[int, int]]]:
        """Generate screen coordinates for maze

        Returns:
            list[list[tuple[int, int]]]: Coordinate matrix
        """

        coords: list[list[tuple[int, int]]] = []

        # Generate coordinates for every cell in maze matrix
        for i in range(self.height):
            row = []

            for j in range(self.width):

                # Calculate coordinates for the cell
                x = j * CELL_SIZE + (CELL_SIZE // 2)
                y = i * CELL_SIZE + HEADER_HEIGHT

                row.append((x, y))

            coords.append(row)

        return coords

    def get_cell_value(self, pos: tuple[int, int]) -> str:
        """Get cell value

        Args:
            pos (tuple[int, int]): Position of the cell

        Returns:
            str: Cell value
        """

        return self.maze[pos[0]][pos[1]].value

    def set_cell(self, pos: tuple[int, int], value: str, forced: bool = False) -> None:
        """Update a cell value in the maze

        Args:
            pos (tuple[int, int]): Position of the cell
            value (str): String value for the cell
            forced (bool): Force set
        """
        if pos in (self.start, self.goal) and not forced:
            return

        match value:
            case "A":
                cost = 0
                self.start = pos
                self.maze[pos[0]][pos[1]].parent = None
            case "B":
                cost = 1
                self.goal = pos
                self.maze[pos[0]][pos[1]].parent = None
            case "#":
                cost = -1
            case "V":
                cost = self.maze[pos[0]][pos[1]].cost
            case "V1":
                cost = self.maze[pos[0]][pos[1]].cost
            case "V2":
                cost = self.maze[pos[0]][pos[1]].cost
            case "*":
                cost = self.maze[pos[0]][pos[1]].cost
            case _:
                cost = int(value)

        self.maze[pos[0]][pos[1]].value = value
        self.maze[pos[0]][pos[1]].cost = cost

    def clear_board(self) -> None:
        """Clear maze walls
        """
        self.maze = [[Node("1", (rowIdx, colIdx), 1)
                      for colIdx in range(self.width)]
                     for rowIdx in range(self.height)]

        self.set_cell(self.start, "A", forced=True)
        self.set_cell(self.goal, "B", forced=True)

    def clear_visited(self) -> None:
        """Clear visited nodes
        """
        for i in range(self.height):
            for j in range(self.width):
                node = self.maze[i][j]
                if node.value in ("V", "*"):
                    self.set_cell((i, j), str(node.cost))

    def mouse_within_bounds(self, pos: tuple[int, int]) -> bool:
        """Check if mouse cursor is inside the maze

        Args:
            pos (tuple[int, int]): Mouse position

        Returns:
            bool: Whether mouse is within the maze
        """
        return all((
            pos[1] > HEADER_HEIGHT,
            pos[1] < 890,
            pos[0] > CELL_SIZE // 2,
            pos[0] < WIDTH - CELL_SIZE // 2
        ))

    def get_cell_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Get cell position from mouse

        Args:
            pos (tuple[int, int]): Mouse position

        Returns:
            tuple[int, int]: Cell position
        """
        x, y = pos

        return ((y - HEADER_HEIGHT) // CELL_SIZE,
                (x - CELL_SIZE // 2) // CELL_SIZE)

    def draw(self) -> None:
        """Draw maze"""

        # Draw every cell on the screen
        for i, row in enumerate(self.maze):
            for j, node in enumerate(row):

                # Determine cell color
                match node.value:
                    case "#":
                        color = DARK
                    case "A":
                        color = RED
                    case "B":
                        color = GREEN
                    case "*":
                        color = YELLOW
                    case "V":
                        color = BLUE
                    case "V1":
                        color = GREEN
                    case "V2":
                        color = DARK_BLUE
                    case _:
                        color = WHITE

                # Cell coordinates
                x, y = self.coords[i][j]
                for node in self.animator.nodes_to_animate:
                    if node.center == (x + 15, y + 15) and node.progress > 0:
                        self._draw_rect(
                            coords=(i, j),
                            color=node.color,
                            node=node
                        )
                        break
                else:
                    self._draw_rect((i, j), color)

    def generate_maze(self, weighted: bool = False) -> None:
        """Generate a new maze using recursive division algorithm
        """
        nodes_to_animate = []
        for i in range(self.width):
            rect = pygame.Rect(0, 0, 9, 9)
            x, y = self.coords[0][i]
            rect.center = (x + 15, y + 15)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        nodes_to_animate = []
        for i in range(self.width):
            rect = pygame.Rect(0, 0, 9, 9)
            x, y = self.coords[-1][i]
            rect.center = (x + 15, y + 15)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        nodes_to_animate = []
        for i in range(self.height):
            rect = pygame.Rect(0, 0, 9, 9)
            x, y = self.coords[i][0]
            rect.center = (x + 15, y + 15)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )

            rect = pygame.Rect(0, 0, 9, 9)
            x, y = self.coords[i][-1]
            rect.center = (x + 15, y + 15)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        self._generate_by_recursive_division(
            1, self.width - 2, 1, self.height - 2)

        if not weighted:
            return

        path = self.solve("A* Search", visualize=False).path
        nodes_to_animate = []
        for rowIdx, row in enumerate(self.maze):
            for colIdx in range(0, len(row), 2):
                if (rowIdx, colIdx) in path:
                    continue

                rect = pygame.Rect(0, 0, 9, 9)
                x, y = self.coords[rowIdx][colIdx]

                exists = False
                for node in self.animator.nodes_to_animate:
                    if node.center == (x + 15, y + 15):
                        exists = True
                        break

                if exists:
                    continue

                nodes_to_animate.append(
                    AnimatingNode(
                        rect=rect,
                        center=(x + 15, y + 15),
                        ticks=pygame.time.get_ticks(),
                        value=str(random.randint(1, 9)),
                        color=WHITE,
                        duration=50
                    )
                )

        self.animator.add_nodes_to_animate(nodes_to_animate, delay=0)

    def _generate_by_recursive_division(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int
    ) -> None:
        """Generate maze by recursive division algorithm

        Args:
            x1 (int): Grid row start
            x2 (int): Grid row end
            y1 (int): Grid column start
            y2 (int): Grid column end
        """
        width = x2 - x1
        height = y2 - y1

        # Base case:
        if width < 1 or height < 1:
            return

        # Whether to draw horizontally or vertically
        horizontal = True if height > width else (
            False if width != height else random.choice((True, False)))

        # Arguments for reursive calls
        args_list: list[tuple[int, int, int, int]] = []

        # Divide the maze and add new grids' properties to args_list
        if horizontal:
            y = self.draw_line(x1, x2, y1, y2, horizontal=True)
            args_list.extend([(x1, x2, y1, y - 1), (x1, x2, y + 1, y2)])
        else:
            x = self.draw_line(x1, x2, y1, y2)
            args_list.extend([(x1, x - 1, y1, y2), (x + 1, x2, y1, y2)])

        # Divide the two grids
        for args in args_list:
            self._generate_by_recursive_division(*args)

    def draw_line(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        horizontal: bool = False
    ) -> int:
        """Draw walls horizontally or vertically

        Args:
            x1 (int): Grid row start
            x2 (int): Grid row end
            y1 (int): Grid column start
            y2 (int): Grid column end
            horizontal (bool, optional): Horizontal or vertical. Defaults to False.

        Returns:
            int: X or Y coordinate of wall line
        """

        # Handle horizontal division
        if horizontal:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Walls at even places
        if x1 % 2 != 0:
            x1 += 1
        wall = random.randrange(x1, x2, 2)

        # Holes at odd places
        if y1 % 2 == 0:
            y1 += 1
        hole = random.randrange(y1, y2, 2)

        # Coordinates
        hole_coords = (hole, wall) if not horizontal else (wall, hole)
        wall_coords = [-1, wall] if not horizontal else [wall, -1]

        # Draw walls
        nodes_to_animate = []
        for i in range(y1, y2 + 1):
            wall_coords[horizontal] = i
            if hole_coords == tuple(wall_coords):
                continue

            # Create a rectangle
            rect = pygame.Rect(0, 0, 9, 9)

            # Set the starting position of the rectangle
            x, y = self.coords[wall_coords[0]][wall_coords[1]]
            rect.center = (x + 15, y + 15)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )
        self.animator.add_nodes_to_animate(nodes_to_animate)

        return wall

    def solve(
        self,
        algo_name: str,
        visualize: bool = True,
    ) -> Solution:
        """Solve the maze with an algorithm

        Args:
            algo_name (str): Name of algorithm
        """
        # String -> Search Algorithm
        mapper: dict[str, Search] = {
            "A* Search": Search.ASTAR_SEARCH,
            "Dijkstra's Search": Search.DIJKSTRAS_SEARCH,
            "Breadth First Search": Search.BREADTH_FIRST_SEARCH,
            "Depth First Search": Search.DEPTH_FIRST_SEARCH,
        }

        # Instantiate Grid for PathFinder
        grid = Grid(self.maze, self.start, self.goal)

        # Solve the maze
        solution = PathFinder.find_path(
            grid=grid,
            search=mapper[algo_name.strip()],
        )

        if not visualize:
            return solution

        nodes = []

        for cell in solution.explored[1:-1]:
            x, y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=pygame.Rect(0, 0, 9, 9),
                    ticks=pygame.time.get_ticks(),
                    value="V",
                    color=YELLOW if "*" in algo_name else GREEN,
                    color_after=BLUE,
                    duration=300
                )
            )

        self.animator.add_nodes_to_animate(nodes, gap=17)

        # Color the solution path in blue
        nodes = []
        for cell in solution.path[1:-1]:
            x, y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=pygame.Rect(0, 0, 9, 9),
                    ticks=pygame.time.get_ticks(),
                    value="*",
                    color=YELLOW,
                    duration=300
                )
            )
        self.animator.add_nodes_to_animate(nodes, gap=34)

        return solution

    def _draw_rect(
            self,
            coords: tuple[int, int],
            color: tuple[int, int, int] = BLUE,
            node: AnimatingNode | None = None
    ) -> None:
        """Color an existing cell in the maze

        Args:
            coords (tuple[int, int]): Cell coordinates
            color (tuple[int, int, int], optional): Color. Defaults to YELLOW.
            delay (bool, optional): Whether to delay after execution. Defaults to False.
        """

        # Determine maze coordinates
        row, col = coords
        x, y = self.coords[row][col]

        if coords in (self.start, self.goal) and color == DARK:
            return

        # Draw
        pygame.draw.rect(
            surface=self.surface,
            color=color,
            rect=node.rect if node else pygame.Rect(
                x, y, CELL_SIZE, CELL_SIZE)
        )

        if color in (BLUE, WHITE, GREEN, DARK_BLUE):
            pygame.draw.rect(
                surface=self.surface,
                color=BLUE if color == YELLOW else GRAY,
                rect=pygame.Rect(x, y, CELL_SIZE, CELL_SIZE),
                width=1
            )

        if (n := self.maze[row][col]).cost > 1:
            image_rect = WEIGHT.get_rect(center=(x + 15, y + 15))
            self.surface.blit(WEIGHT, image_rect)

            text = FONT.render(
                str(n.cost if not node else node.value), True, GRAY
            )
            text_rect = text.get_rect()
            text_rect.center = image_rect.center
            self.surface.blit(text, text_rect)
