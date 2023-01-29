import math
import pygame

from .constants import DARK, GRAY, WHITE


class AnimatingNode:
    def __init__(
        self,
        center: tuple[int, int],
        rect: pygame.Rect,
        ticks: int,
        value: str,
        color: tuple[int, int, int],
        duration: int = 300
    ) -> None:
        self.rect = rect
        self.ticks = ticks
        self.value = value
        self.color = color
        self.progress = 0
        self.duration = duration
        self.center = center

    def __repr__(self) -> str:
        return f"AnimatingNode{tuple(vars(self).values())}"

    def __str__(self) -> str:
        return f"AnimatingNode: Value: {self.value}, " \
            + f"Progress: {self.progress}/{self.duration}"


class Animator:
    def __init__(self, surface: pygame.surface.Surface, maze) -> None:
        self.surface = surface
        self.maze = maze

        self.animating = False
        self.nodes_to_animate: list[AnimatingNode] = []

    def add_nodes_to_animate(self, nodes: list[AnimatingNode], delay=False):
        """Add nodes for animation

        Args:
            nodes (list[AnimatingNode]): List of nodes
            delay (bool, optional): Whether to wait for previous nodes to animate. Defaults to False.
        """

        # Update first node's ticks and add it to the list
        if len(self.nodes_to_animate):
            nodes[0].ticks = self.nodes_to_animate[-1].ticks + 5
            if delay:
                nodes[0].ticks += 40

        self.nodes_to_animate.append(nodes[0])

        # Rest of the nodes
        for i in range(1, len(nodes)):
            nodes[i].ticks = nodes[i - 1].ticks + 5
            self.nodes_to_animate.append(nodes[i])

    def animate_walls(self):
        """Animate nodes in the nodes_to_animate list
        """
        if not self.nodes_to_animate:
            return

        for idx, node in enumerate(self.nodes_to_animate):
            node.progress += pygame.time.get_ticks() - node.ticks
            node.ticks = pygame.time.get_ticks()

            if node.progress < 0:
                node.progress = 0
                return

            if node.progress < node.duration / 2:
                size = self._easeOutExpo(
                    node.progress, 9, 36 - 9, node.duration / 2
                )
            else:
                size = self._easeOutExpo(
                    node.progress - node.duration / 2,
                    36, 30 - 36, node.duration / 2
                )

            node.rect.width = node.rect.height = int(size)
            node.rect.center = node.center

            if node.progress >= node.duration:
                pos = self.maze.get_cell_pos(node.rect.topleft)
                if self.maze.get_cell_value(pos) != "#":
                    self.maze.set_cell(pos, node.value)

                self.nodes_to_animate.pop(idx)

            if node.color == WHITE:
                pygame.draw.rect(self.surface, GRAY, node.rect)
                pygame.draw.rect(self.surface, DARK, node.rect, width=8)
            else:
                pygame.draw.rect(self.surface, node.color, node.rect)

    def _easeOutExpo(
        self,
        time: float,
        starting_value: float,
        change_in_value: float,
        duration: float
    ) -> float:
        """Calculate current size

        Args:
            time (float): The current time of the animation.
            starting_value (float): The starting value of the animation.
            change (float): The change in value of the animation.
            duration (float): The total duration of the animation in milliseconds.

        Returns:
            float: Current value
        """
        return change_in_value * (-math.pow(2, -10 * time / duration) + 1) \
            + starting_value

    def __repr__(self) -> str:
        return f"Animator{tuple(vars(self).values())}"
