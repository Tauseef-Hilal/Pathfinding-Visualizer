import time
import pygame
from src.button import Button

from src.unnamed.base import Node
from src.unnamed.dfs import QueueFrontier

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
    def __init__(self, surface):
        self.maze = self._generate_maze()
        self.width = max(len(row) for row in self.maze)
        self.height = len(self.maze)
        self.coords = self._generate_coordinates()
        self.surface = surface

    def _generate_maze(self):
        maze: list[list[str]] = []
        filename = "data/maze/maze2.txt"
        # filename = f"data/maze/maze{str(choice((1, 2, 3)))}.txt"

        with open(filename) as file:
            content = file.read()

            for i, line in enumerate(content.splitlines()):
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

    def solve(self):
        node = Node(state=self.start, parent=None, action=None)

        frontier = QueueFrontier()
        frontier.add(node)

        explored_states = set()

        while True:
            pygame.time.delay(100)
            if frontier.empty():
                msg = Button("NO SOLUTION!", "center", "center",
                             12, 70, pygame.Color(*RED), pygame.Color(*DARK))
                msg.draw(surf=self.surface)
                pygame.display.update()

                return False

            if node.parent:
                self._draw_rect(coords=node.state)
                pygame.display.update()

            node = frontier.remove()

            if node.state == self.goal:
                cells = set()
                temp = node.parent
                while temp.parent != None:
                    cells.add(temp.state)
                    temp = temp.parent

                for cell in explored_states:
                    if cell in cells:
                        self._draw_rect(coords=cell, color=BLUE)
                        continue

                    self._draw_rect(coords=cell, color=REDLIKE)

                pygame.display.update()

                return True

            explored_states.add(node.state)

            for action, state in self._get_actions(node.state).items():
                new = Node(
                    state=state,
                    parent=node,
                    action=action
                )

                if state in explored_states or frontier.contains_state(state):
                    continue
                frontier.add(node=new)

    def _draw_rect(self, coords: tuple[int, int], color: tuple = YELLOW):
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

    def _get_actions(self, state) -> dict[str, tuple[int, int]]:
        row, col = state
        action_state_mapper = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1),
        }

        possible_actions = {}
        for action, (r, c) in action_state_mapper.items():
            if not (0 <= r < self.height and 0 <= c < self.width):
                continue

            if self.maze[r][c] == "#":
                continue

            possible_actions[action] = (r, c)

        return possible_actions
