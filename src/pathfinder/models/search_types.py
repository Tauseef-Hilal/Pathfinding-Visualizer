from enum import Enum


class Search(Enum):
    """Enum for search algorithms"""

    BREADTH_FIRST_SEARCH = "BFS"
    DEPTH_FIRST_SEARCH = "DFS"
    ASTAR_SEARCH = "A*"
