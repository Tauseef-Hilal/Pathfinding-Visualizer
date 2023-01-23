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

        self.start = (0, 0)
        self.maze[0][0] = "A"
        self.goal = (self.width, self.height)
        self.maze[self.height - 1][self.width - 1] = "B"

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

    def set_cell(self, pos: tuple[int, int], value: str) -> None:
        """Update a cell value in the maze

        Args:
            pos (tuple[int, int]): Position of the cell
            value (str): String value for the cell
        """

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
            self.start = start

        if goal:
            self.goal = goal

    def clear_walls(self) -> None:
        """Clear maze walls
        """
        self.maze = [[" " for _ in range(self.width)]
                     for _ in range(self.height)]
        self.maze[self.start[0]][self.start[1]] = "A"
        self.maze[self.goal[0]][self.goal[1]] = "B"

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
                    case _:
                        color = WHITE

                # Cell coordinates
                # x, y = self.coords[i][j]
                self._draw_rect((i, j), color)

    def solve(self, algo_name: str) -> None:
        """Solve the maze with an algorithm

        Args:
            algo_name (str): Name of algorithm
        """
        # String -> Search Algorithm
        mapper: dict[str, Search] = {
            "Breadth First Search": Search.BREADTH_FIRST_SEARCH,
            "Depth First Search": Search.DEPTH_FIRST_SEARCH,
            "A*  Search": Search.ASTAR_SEARCH,
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
                self._draw_rect(coords=cell, color=YELLOW)
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

        # Wait for 50ms
        if delay:
            pygame.time.delay(20)
            pygame.display.update()
