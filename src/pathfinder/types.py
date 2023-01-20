from typing import Optional, Protocol
from src.pathfinder.models.grid import Grid

from src.pathfinder.models.solution import NoSolution, Solution


class Visualiser(Protocol):
    def __call__(
        self,
        coords: tuple[int, int],
        color: tuple[int, int, int] = (220, 235, 113),
        delay: bool = False
    ) -> None:
        return


class SearchFunction(Protocol):
    def __call__(
        self,
        grid: Grid,
        callback:
        Optional[Visualiser] = None
    ) -> Solution:
        return NoSolution([], 0)
