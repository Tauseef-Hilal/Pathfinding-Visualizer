from enum import Enum


class Search(Enum):
    """Enum for search algorithms"""

    ASTAR_SEARCH = "A*"
    DIJKSTRAS_SEARCH = "DS"
    BREADTH_FIRST_SEARCH = "BFS"
    GREEDY_BEST_FIRST_SEARCH = "GBFS"
    DEPTH_FIRST_SEARCH = "DFS"
