import pygame

from .constants import (
    CELL_SIZE,
    DARK,
    WHITE,
    GREEN,
    BLACK,
    RED,
    WIDTH,
    HEIGHT,
)


class Maze:
    def __init__(self):
        self.maze, self.walls = self._generate_maze()
        self.width = max(len(row) for row in self.maze) * CELL_SIZE
        self.height = len(self.maze) * CELL_SIZE

    def _generate_maze(self):
        maze: list[list[str]] = []
        walls: list[list[bool]] = []
        filename = "data/maze/maze2.txt"
        # filename = f"data/maze/maze{str(choice((1, 2, 3)))}.txt"

        with open(filename) as file:
            content = file.read()

            for i, line in enumerate(content.splitlines()):
                maze.append(list(line))

                # row = []
                # for j, char in enumerate(line):
                #     match char:
                #         case "#":
                #             row.append(True)
                #         case "A":
                #             self.start = (i, j)
                #             row.append(False)
                #         case "B":
                #             self.goal = (i, j)
                #             row.append(False)
                #         case _:
                #             row.append(False)

                # walls.append(row)

        return maze, walls

    def draw(self, window):
        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                match col:
                    case "#":
                        color = DARK
                    case "A":
                        color = RED
                    case "B":
                        color = GREEN
                    case _:
                        color = WHITE

                pygame.draw.rect(
                    surface=window,
                    color=color,
                    rect=pygame.Rect(
                        j * CELL_SIZE + ((WIDTH - self.width) / 2),
                        i * CELL_SIZE + ((HEIGHT - self.height) / 2),
                        CELL_SIZE,
                        CELL_SIZE
                    ),
                )

                pygame.draw.rect(
                    surface=window,
                    color=BLACK,
                    rect=pygame.Rect(
                        j * CELL_SIZE + ((WIDTH - self.width) / 2),
                        i * CELL_SIZE + ((HEIGHT - self.height) / 2),
                        CELL_SIZE,
                        CELL_SIZE
                    ),
                    width=1
                )

    