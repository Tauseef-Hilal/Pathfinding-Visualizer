import pygame

from .button import Button
from .pathfinder.main import PathFinder
from .pathfinder.models.grid import Grid
from .pathfinder.models.search_types import Search

from .constants import (
    CELL_SIZE,
    WIDTH,
    HEIGHT,
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
    def __init__(self, surface: pygame.surface.Surface, filename: str) -> None:
        self.surface = surface

        # Generate maze from file
        self.maze = self._generate_maze(filename)

        # Calculate maze width and height
        self.width = max(len(row) for row in self.maze)
        self.height = len(self.maze)

        # Generate screen coordinates for maze
        self.coords = self._generate_coordinates()

    def _generate_maze(self, filename: str) -> list[list[str]]:
        """Generate maze from file

        Args:
            filename (str): Maze file name

        Returns:
            list[list[str]]: Maze matrix
        """

        maze: list[list[str]] = []

        # Read from file and populate maze
        with open(filename) as file:
            content = file.read()

            for line in content.splitlines():
                maze.append(list(line))

        return maze

    def _generate_coordinates(self) -> list[list[tuple[float, float]]]:
        """Generate screen coordinates for maze

        Returns:
            list[list[tuple[float, float]]]: Coordinate matrix
        """

        coords: list[list[tuple[float, float]]] = []

        # Generate coordinates for every cell in maze matrix
        for i in range(len(self.maze)):
            row = []

            for j in range(len(self.maze[i])):

                # Calculate coordinates for the cell
                x = j * CELL_SIZE + ((WIDTH - self.width * CELL_SIZE) / 2)
                y = i * CELL_SIZE + ((HEIGHT - self.height * CELL_SIZE) / 2)

                row.append((x, y))

            coords.append(row)

        return coords

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
                x, y = self.coords[i][j]

                # Draw
                pygame.draw.rect(
                    surface=self.surface,
                    color=color,
                    rect=pygame.Rect(
                        x,
                        y,
                        CELL_SIZE,
                        CELL_SIZE
                    ),
                )

                pygame.draw.rect(
                    surface=self.surface,
                    color=BLACK,
                    rect=pygame.Rect(
                        x,
                        y,
                        CELL_SIZE,
                        CELL_SIZE
                    ),
                    width=1
                )

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
                self._draw_rect(coords=cell, color=BLUE)

            # Color other explored cells in red
            explored = list(solution.explored)
            path = set(solution.path)

            for cell in explored:
                if cell not in path:
                    self._draw_rect(coords=cell, color=REDLIKE)

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
            color: tuple[int, int, int] = YELLOW,
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

        pygame.draw.rect(
            surface=self.surface,
            color=BLACK,
            rect=pygame.Rect(x, y, CELL_SIZE, CELL_SIZE),
            width=1
        )

        # Wait for 50ms
        if delay:
            pygame.time.delay(50)
            pygame.display.update()
