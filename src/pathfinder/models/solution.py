class Solution:
    """Model a solution to a pathfinding problem"""

    def __init__(
        self,
        path: list[tuple[int, int]],
        explored: set[tuple[int, int]]
    ) -> None:
        self.path = path
        self.explored = explored

    def __repr__(self) -> str:
        return f"Solution([{self.path[0]}, ..., {self.path[-1]}], [...])"


class NoSolution(Solution):
    """Model an empty pathfinding solution"""
    pass
