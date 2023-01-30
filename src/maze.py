import random
import pygame

from .animations import AnimatingNode, Animation, Animator
from .pathfinder.models.node import Node
from .pathfinder.models.solution import Solution
from .pathfinder.main import PathFinder
from .pathfinder.models.grid import Grid
from .pathfinder.models.search_types import Search

from .constants import (
    GOAL,
    START,
    WEIGHT,
    CELL_SIZE,
    DARK_BLUE,
    FONT_14,
    GRAY,
    GREEN_2,
    MAZE_HEIGHT,
    HEADER_HEIGHT,
    MAZE_WIDTH,
    PURPLE,
    WIDTH,
    BLUE,
    DARK,
    WHITE,
    GREEN,
    YELLOW
)


class MazeNode(Node):
    def __init__(
        self,
        value: str,
        state: tuple[int, int],
        cost: int,
        parent: Node | None = None,
        action: str | None = None,
        color: tuple[int, int, int] = WHITE
    ) -> None:
        super().__init__(value, state, cost, parent, action)
        self.color = color


class Maze:
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface
        self.animator: Animator

        self.width = MAZE_WIDTH // CELL_SIZE
        self.height = MAZE_HEIGHT // CELL_SIZE

        self.maze = [[MazeNode("1", (rowIdx, colIdx), 1)
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
            if value == "V":
                self.maze[pos[0]][pos[1]].color = BLUE
            elif value == "*":
                self.maze[pos[0]][pos[1]].color = YELLOW
            return

        match value:
            case "A":
                color = WHITE
                cost = 0
                self.start = pos
                self.maze[pos[0]][pos[1]].parent = None
            case "B":
                color = WHITE
                cost = 1
                self.goal = pos
                self.maze[pos[0]][pos[1]].parent = None
            case "#":
                cost = -1
                color = DARK
            case "V":
                cost = self.maze[pos[0]][pos[1]].cost
                color = BLUE
            case "*":
                cost = self.maze[pos[0]][pos[1]].cost
                color = YELLOW
            case _:
                cost = int(value)
                color = WHITE

        self.maze[pos[0]][pos[1]].value = value
        self.maze[pos[0]][pos[1]].cost = cost
        self.maze[pos[0]][pos[1]].color = color

    def clear_board(self) -> None:
        """Clear maze walls
        """
        self.maze = [[MazeNode("1", (rowIdx, colIdx), 1)
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
                if node.value in ("V", "*", "V1", "V2"):
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
                x, y = self.coords[i][j]

                for animating_node in self.animator.nodes_to_animate:
                    if animating_node.center == (x + 15, y + 15) \
                            and animating_node.progress > 0:

                        self._draw_rect(
                            coords=(i, j),
                            color=animating_node.color,
                            node=animating_node
                        )
                        break

                else:
                    self._draw_rect((i, j), node.color)

    def generate_maze(self, weighted: bool = False) -> None:
        """Generate a new maze using recursive division algorithm
        Create an animated node for each wall and add that to 
        `animator.nodes_to_animate` list
        """

        # Top horizontal
        nodes_to_animate = []
        for i in range(self.width):
            x, y = self.coords[0][i]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, 9, 9),
                    center=(x + 15, y + 15),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        # Bottom horizontal
        nodes_to_animate = []
        for i in range(self.width):
            x, y = self.coords[-1][i]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, 9, 9),
                    center=(x + 15, y + 15),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        # Sides
        nodes_to_animate = []
        for i in range(self.height):
            x, y = self.coords[i][0]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, 9, 9),
                    center=(x + 15, y + 15),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

            x, y = self.coords[i][-1]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, 9, 9),
                    center=(x + 15, y + 15),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        # Recursive division algorithm
        self._generate_by_recursive_division(
            1, self.width - 2, 1, self.height - 2)

        # Return if need normal maze
        if not weighted:
            return

        # Calculate optimal path
        path = self.solve("A* Search", visualize=False).path

        # Place weighted nodes randomly skipping walls and optimal path nodes
        nodes_to_animate = []
        for rowIdx, row in enumerate(self.maze):
            for colIdx in range(0, len(row), 2):
                if (rowIdx, colIdx) in path:
                    continue

                x, y = self.coords[rowIdx][colIdx]

                for node in self.animator.nodes_to_animate:
                    if node.center == (x + 15, y + 15):
                        break
                else:
                    nodes_to_animate.append(
                        AnimatingNode(
                            rect=pygame.Rect(0, 0, 9, 9),
                            center=(x + 15, y + 15),
                            value=str(random.randint(1, 9)),
                            ticks=pygame.time.get_ticks(),
                            animation=Animation.WEIGHT_ANIMATION,
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
        grid = Grid(self.maze, self.start, self.goal)  # type: ignore

        # Solve the maze
        solution = PathFinder.find_path(
            grid=grid,
            search=mapper[algo_name.strip()],
        )

        if not visualize:
            return solution

        # Animate solution nodes
        nodes = []
        for cell in solution.explored:
            x, y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=pygame.Rect(0, 0, 30, 30),
                    ticks=pygame.time.get_ticks(),
                    value="V",
                    color=WHITE,
                    colors=[YELLOW, PURPLE, GREEN_2, BLUE],
                    duration=2000,
                    animation=Animation.PATH_ANIMATION
                )
            )

        self.animator.add_nodes_to_animate(nodes, gap=10)

        # Color the shortest path in yellowd
        nodes = []
        for cell in solution.path:
            x, y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + 15, y + 15),
                    rect=pygame.Rect(0, 0, 9, 9),
                    ticks=self.animator.nodes_to_animate[0].ticks,
                    value="*",
                    color=YELLOW,
                    duration=300
                )
            )

        self.animator.add_nodes_to_animate(nodes, delay=1500, gap=30)

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

        # Draw border if needed
        if color in (BLUE, WHITE, GREEN) or \
                (node and node.color == YELLOW):
            pygame.draw.rect(
                surface=self.surface,
                color=GREEN if color == GREEN_2 else GRAY,
                rect=pygame.Rect(x, y, CELL_SIZE, CELL_SIZE),
                width=1
            )

        # Draw images if needed
        if (n := self.maze[row][col]).cost > 1:
            image_rect = WEIGHT.get_rect(center=(x + 15, y + 15))
            self.surface.blit(WEIGHT, image_rect)

            text = FONT_14.render(
                str(n.cost if not node else node.value), True, GRAY
            )
            text_rect = text.get_rect()
            text_rect.center = image_rect.center
            self.surface.blit(text, text_rect)

        elif (row, col) == self.start:
            image_rect = START.get_rect(center=(x + 15, y + 15))
            self.surface.blit(START, image_rect)

        elif (row, col) == self.goal:
            image_rect = GOAL.get_rect(center=(x + 15, y + 15))
            self.surface.blit(GOAL, image_rect)
