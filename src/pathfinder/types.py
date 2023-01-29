from typing import Optional, Protocol

from .models.grid import Grid
from .models.solution import NoSolution, Solution


class Visualiser(Protocol):
    def __call__(
        self,
        coords: tuple[int, int],
        color: tuple[int, int, int] = (220, 235, 113),
        delay: bool = False
    ) -> None:
        """Callback for visualisation. Run every new cell traversal

        Args:
            coords (tuple[int, int]): Cell coordinates
            color (tuple[int, int, int], optional): Color. Defaults to 
            (220, 235, 113).
            delay (bool, optional): Delay after execution. Defaults to False.
        """
        return


class SearchFunction(Protocol):
    def __call__(
        self,
        grid: Grid,
    ) -> Solution:
        """Find path between two points in a grid using a searching algorithm

        Args:
            grid (Grid): Grid of points
            callback (Optional[Visualiser], optional): Callback for 
            visualisation. Defaults to None.

        Returns:
            Solution: Solution found
        """
        return NoSolution([], [])
