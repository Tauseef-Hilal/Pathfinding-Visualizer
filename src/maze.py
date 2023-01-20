import pygame

from .button import Button
from .pathfinder.models.search_types import Search
from .pathfinder.models.grid import Grid
from .pathfinder.main import PathFinder

from .constants import (
    BLUE,
    CELL_SIZE,
    DARK,
    REDLIKE,
    WHITE,
    GREEN,
    BLACK,
    RED,
    YELLOW,
    WIDTH,
    HEIGHT,
)


class Maze:
    def __init__(self, surface, filename):
        self.maze = self._generate_maze(filename)
        self.width = max(len(row) for row in self.maze)
        self.height = len(self.maze)
        self.coords = self._generate_coordinates()
        self.surface = surface

    def _generate_maze(self, filename):
        maze: list[list[str]] = []

        with open(filename) as file:
            content = file.read()

            for line in content.splitlines():
                maze.append(list(line))

        return maze

    def _generate_coordinates(self):
        coords: list[list[tuple[float, float]]] = []

        for i in range(len(self.maze)):
            row = []

            for j in range(len(self.maze[i])):
                x = j * CELL_SIZE + ((WIDTH - self.width * CELL_SIZE) / 2)
                y = i * CELL_SIZE + ((HEIGHT - self.height * CELL_SIZE) / 2)
                row.append((x, y))

            coords.append(row)

        return coords

    def draw(self):
        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
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

                x, y = self.coords[i][j]

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

    def solve(self, algo_name: str):
        mapper: dict[str, Search] = {
            "Breadth First Search": Search.BREADTH_FIRST_SEARCH,
            "Depth First Search": Search.DEPTH_FIRST_SEARCH,
        }
        grid = Grid(self.maze, self.start, self.goal)
        solution = PathFinder.find_path(
            grid=grid,
            search=mapper[algo_name.strip()],
            callback=self._draw_rect
        )

        if solution.path:
            for cell in solution.path[1:-1]:
                self._draw_rect(coords=cell, color=BLUE)
                
            explored = list(solution.explored)
            path = set(solution.path)
            for cell in explored:
                if cell not in path:
                    self._draw_rect(coords=cell, color=REDLIKE)

            pygame.display.update()
            return

        msg = Button(
            "NO SOLUTION!", "center", "center",
            12, 70, foreground_color=pygame.Color(*RED), background_color=pygame.Color(*DARK)
        )

        msg.draw(surf=self.surface)
        pygame.display.update()

    def _draw_rect(self, coords: tuple[int, int], color=YELLOW, delay=False):
        row, col = coords
        x, y = self.coords[row][col]

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

        if delay:
            pygame.time.delay(50)
            pygame.display.update()
