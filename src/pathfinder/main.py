from .types import Visualiser
from .search.bfs import BreadthFirstSearch
from .models.search_types import Search
from .models.grid import Grid
from .models.solution import Solution


class PathFinder:
    @staticmethod
    def find_path(
            grid: Grid,
            search: Search,
            callback: Visualiser
    ) -> Solution:
        return BreadthFirstSearch.search(grid, callback)
