class Solution:
    """Model a solution to a pathfinding problem"""

    def __init__(
        self,
        path: list[tuple[int, int]],
        explored: list[tuple[int, int]],
        time: float
    ) -> None:
        self.path = path
        self.explored = explored
        self.time = time

    def __repr__(self) -> str:
        return f"Solution([{self.path[0]}, ..., {self.path[-1]}], {'{...}'}, {self.time})"


class NoSolution(Solution):
    """Model an empty pathfinding solution"""

    def __repr__(self) -> str:
        explored = list(self.explored)
        return f"Solution([], {'{'}{explored[0]}, {explored[1]}, ...{'}'}, {self.time})"
