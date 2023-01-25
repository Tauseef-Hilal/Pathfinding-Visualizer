import random
import time
from typing import Optional
import pygame

from .button import Button
from .pathfinder.main import PathFinder
from .pathfinder.models.grid import Grid
from .pathfinder.models.search_types import Search

from .constants import (
    CELL_SIZE,
    GRAY,
    MAZE_HEIGHT,
    HEADER_HEIGHT,
    MAZE_WIDTH,
    WIDTH,
    BLUE,
    DARK,
    REDLIKE,
    WHITE,
    GREEN,
    BLACK,
    RED,
    YELLOW
)


class Maze:
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface

        self.width = MAZE_WIDTH // CELL_SIZE
        self.height = MAZE_HEIGHT // CELL_SIZE

        self.maze = [[" " for _ in range(self.width)]
                     for _ in range(self.height)]

        self.start = (10, self.height // 2)
        self.maze[self.start[1]][self.start[0]] = "A"
        self.goal = (self.width - 11, self.height // 2)
        self.maze[self.goal[1]][self.goal[0]] = "B"

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

        return self.maze[pos[0]][pos[1]]

    def set_cell(self, pos: tuple[int, int], value: str, forced: bool = False) -> None:
        """Update a cell value in the maze

        Args:
            pos (tuple[int, int]): Position of the cell
            value (str): String value for the cell
        """
        if pos in (self.start, self.goal) and not forced:
            return

        self.maze[pos[0]][pos[1]] = value

    def update_ends(
        self,
        start: Optional[tuple[int, int]] = None,
        goal: Optional[tuple[int, int]] = None
    ) -> None:
        """Update maze ends (start and goal)

        Args:
            start (Optional[tuple[int, int]], optional): Maze start. Defaults to None.
            end (Optional[tuple[int, int]], optional): Maze end. Defaults to None.
        """
        if start:
            self.maze[start[0]][start[1]] = "A"
            self.start = start

        if goal:
            self.maze[goal[0]][goal[1]] = "B"
            self.goal = goal

    def clear_walls(self) -> None:
        """Clear maze walls
        """
        self.maze = [[" " for _ in range(self.width)]
                     for _ in range(self.height)]
        self.maze[self.start[0]][self.start[1]] = "A"
        self.maze[self.goal[0]][self.goal[1]] = "B"

    def clear_visited(self) -> None:
        """Clear visited nodes
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.get_cell_value((i, j)) in ("V", "*"):
                    self.set_cell((i, j), " ")

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
            for j, col in enumerate(row):

                # Determine cell color
                match col:
                    case "#":
                        color = DARK
                    case "A":
                        color = RED
                        self.start = (i, j)
                    case "B":
                        color = GREEN
                        self.goal = (i, j)
                    case "*":
                        color = YELLOW
                    case "V":
                        color = BLUE
                    case _:
                        color = WHITE

                # Cell coordinates
                self._draw_rect((i, j), color)

    def generate_maze(self) -> None:
        """Generate a new maze using recursive division algorithm
        """
        for i in range(self.width):
            self.set_cell((0, i), "#")
            self.set_cell((-1, i), "#")
            self._draw_rect((0, i), DARK, delay=True)
            self._draw_rect((-1, i), DARK, delay=True)

        for i in range(self.height):
            self.set_cell((i, 0), "#")
            self.set_cell((i, -1), "#")
            self._draw_rect((i, 0), DARK, delay=True)
            self._draw_rect((i, -1), DARK, delay=True)

        self._generate_by_recursive_division(
            1, self.width - 2, 1, self.height - 2)

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
        for i in range(y1, y2 + 1):
            wall_coords[horizontal] = i
            if hole_coords == tuple(wall_coords):
                continue

            self._draw_rect(tuple(wall_coords), DARK, delay=True)

        return wall

    def solve(self, algo_name: str) -> None:
        """Solve the maze with an algorithm

        Args:
            algo_name (str): Name of algorithm
        """
        # String -> Search Algorithm
        mapper: dict[str, Search] = {
            "Breadth First Search": Search.BREADTH_FIRST_SEARCH,
            "Depth First Search": Search.DEPTH_FIRST_SEARCH,
            "A* Search": Search.ASTAR_SEARCH,
        }

        # Instantiate Grid for PathFinder
        grid = Grid(self.maze, self.start, self.goal)

        # Solve the maze
        solution = PathFinder.find_path(
            grid=grid,
            search=mapper[algo_name.strip()],
            callback=self._draw_rect
        )

        # If found a solution
        if solution.path:

            # Color the solution path in blue
            for cell in solution.path[1:-1]:
                self._draw_rect(coords=cell, color=YELLOW, delay=True)
            pygame.display.update()
            return

        # Otherwise
        msg = Button(
            "NO SOLUTION!", "center", "center",
            12, 70, foreground_color=pygame.Color(*RED), background_color=pygame.Color(*DARK)
        )

        msg.draw(surf=self.surface)
        pygame.display.update()

    def _draw_rect(
            self,
            coords: tuple[int, int],
            color: tuple[int, int, int] = BLUE,
            delay: bool = False
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
            rect=pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        )

        if color == BLUE or color == WHITE:
            pygame.draw.rect(
                surface=self.surface,
                color=GRAY,
                rect=pygame.Rect(x, y, CELL_SIZE, CELL_SIZE),
                width=1
            )

        # Wait for 20ms
        if delay:
            if color != DARK:
                self.set_cell((row, col), "V" if color == BLUE else "*")
                pygame.time.delay(20)
            else:
                self.set_cell((row, col), "#")
                pygame.time.delay(10)

            pygame.display.update()
