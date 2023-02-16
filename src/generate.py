import random
from typing import Any, Callable
import pygame

from .animations import AnimatingNode, Animation, Animator
from .constants import CELL_SIZE, DARK, GREEN_2, BLUE_2, MIN_SIZE, WHITE


GenerationCallback = Callable[[], None]


class MazeGenerator:

    def __init__(self, animator: Animator) -> None:
        from .maze import Maze

        self.animator = animator
        self.maze: Maze = animator.maze

    def _is_valid_cell(self, pos: tuple[int, int]) -> bool:
        """Check if the provided coords are valid

        Args:
            pos (tuple[int, int]): Cell pos

        Returns:
            bool: Whether the cell exists
        """
        rowIdx, colIdx = pos

        return 0 <= rowIdx < self.maze.height \
            and 0 <= colIdx < self.maze.width

    def _get_two_step_neighbors(
        self,
        maze: list[list[Any]],
        cell: tuple[int, int],
        value: str = ""
    ) -> list[tuple[int, int]]:
        """Get neighbors of a cell which are two steps away

        Args:
            cell (tuple[int, int]): Cell pos
            value (str): A string representing the neighbor type. `#` for a wall

        Returns:
            list[tuple[int, int]]: List of neighbors
        """
        neighbors = [(cell[0] + 2, cell[1]),
                     (cell[0] - 2, cell[1]),
                     (cell[0], cell[1] + 2),
                     (cell[0], cell[1] - 2)]

        if value == "#":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] == "#"]
        elif value == "1":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] != "#"]

        return [neighbor for neighbor in neighbors
                if self._is_valid_cell(neighbor)]

    def randomised_prims_algorithm(self) -> None:
        """Generate maze by Randomised Prim's algorithm
        """

        # Create a simpler copy of the actual maze
        maze = [["#" for __ in range(self.maze.width)]
                for _ in range(self.maze.height)]

        maze[self.maze.start[0]][self.maze.start[1]] = "1"
        maze[self.maze.goal[0]][self.maze.goal[1]] = "1"

        # Put walls everywhere
        for rowIdx in range(self.maze.height):
            for colIdx in range(self.maze.width):
                self.maze.set_cell((rowIdx, colIdx), "#")

        # Create a list for storing frontier cells
        frontier = self._get_two_step_neighbors(maze, self.maze.start, "#")

        # Visited frontier cells
        visited = set()

        # For animating nodes
        nodes_to_animate = []

        while frontier:
            cell = random.choice(frontier)

            # Skip if already visited
            if cell in visited:
                frontier.remove(cell)
                continue

            # Get neighbors of type "1"
            neighbors = self._get_two_step_neighbors(maze, cell, "1")

            # If neighbors is not empty, break the wall between the neighbor
            # and the frontier cell. Also set neighbor to type "1"
            if neighbors:
                neighbor = random.choice(neighbors)

                wall = ((cell[0] + neighbor[0]) // 2,
                        (cell[1] + neighbor[1]) // 2)

                maze[wall[0]][wall[1]] = "1"
                maze[cell[0]][cell[1]] = "1"

                # For animations
                x, y = self.maze.coords[wall[0]][wall[1]]
                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=BLUE_2
                    )
                )

                x, y = self.maze.coords[cell[0]][cell[1]]
                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=GREEN_2
                    )
                )

                frontier.extend(self._get_two_step_neighbors(maze, cell, "#"))

            # Add current frontier cell to the visited cell
            # and remove it from the frontier
            visited.add(cell)
            frontier.remove(cell)

        # Add nodes for animation
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

    def randomised_dfs(self) -> None:
        """Generate maze by randomised dfs
        """

        # For animating nodes
        nodes_to_animate = []

        # Draw Walls everywhere except the start and goal pos
        for rowIdx in range(self.maze.height):
            for colIdx in range(self.maze.width):
                self.maze.set_cell((rowIdx, colIdx), "#")

        stack = [self.maze.start]

        visited = set()
        visited.add(self.maze.start)

        while stack:
            # Pop one cell from the stack
            curr = stack.pop()

            # Get unvisited two step neighbors of current cell
            neighbors = self._get_two_step_neighbors(self.maze.maze, curr)
            unvisited_neighbors = [neighbor for neighbor in neighbors
                                   if neighbor not in visited]

            # If the cell has unvisited neighbors, push it to the stack
            # Choose one neighbor and break wall between the neighbor
            # and the current cell. Also set the neighbor to type "1"
            if unvisited_neighbors:
                next = random.choice(unvisited_neighbors)
                stack.append(curr)

                x, y = self.maze.coords[next[0]][next[1]]
                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=BLUE_2
                    )
                )

                rowIdx = (curr[0] + next[0]) // 2
                colIdx = (curr[1] + next[1]) // 2
                x, y = self.maze.coords[rowIdx][colIdx]

                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=GREEN_2,
                    )
                )

                # Add the neighbor to the visited set and push it
                # to the stack
                visited.add(next)
                stack.append(next)

        # Add animating nodes for animation
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

    def basic_weight_maze(self) -> None:
        """Generate a basic weight maze
        """

        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                if random.randint(1, 10) < 8:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value="9",
                        color=WHITE,
                        animation=Animation.WEIGHT_ANIMATION
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)

    def basic_random_maze(self) -> None:
        """Generate a basic random maze
        """
        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                if random.randint(1, 10) < 8:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value="#",
                        color=DARK
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)

    def recursive_division(
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
            y = self._draw_line(x1, x2, y1, y2, horizontal=True)
            args_list.extend([(x1, x2, y1, y - 1), (x1, x2, y + 1, y2)])
        else:
            x = self._draw_line(x1, x2, y1, y2)
            args_list.extend([(x1, x - 1, y1, y2), (x + 1, x2, y1, y2)])

        # Divide the two grids
        for args in args_list:
            self.recursive_division(*args)

    def _draw_line(
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
            rect = pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE)

            # Set the starting position of the rectangle
            x, y = self.maze.coords[wall_coords[0]][wall_coords[1]]
            rect.center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

        return wall
