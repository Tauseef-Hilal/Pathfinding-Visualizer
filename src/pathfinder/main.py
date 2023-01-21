from .models.grid import Grid
from .models.solution import Solution
from .models.search_types import Search
from .search.dfs import DepthFirstSearch
from .search.bfs import BreadthFirstSearch
from .search.astar import AStarSearch
from .types import SearchFunction, Visualiser

SEARCH: dict[Search, SearchFunction] = {
    Search.BREADTH_FIRST_SEARCH: BreadthFirstSearch.search,
    Search.DEPTH_FIRST_SEARCH: DepthFirstSearch.search,
    Search.ASTAR_SEARCH: AStarSearch.search,
}


class PathFinder:
    @staticmethod
    def find_path(
            grid: Grid,
            search: Search,
            callback: Visualiser
    ) -> Solution:
        return SEARCH[search](grid=grid, callback=callback)
