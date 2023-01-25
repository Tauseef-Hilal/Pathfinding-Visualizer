from enum import Enum


class Search(Enum):
    """Enum for search algorithms"""

    ASTAR_SEARCH = "A*"
    DIJKSTRAS_SEARCH = "DS"
    BREADTH_FIRST_SEARCH = "BFS"
    DEPTH_FIRST_SEARCH = "DFS"
