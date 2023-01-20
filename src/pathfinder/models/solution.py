class Solution:
    def __init__(
        self, 
        path: list[tuple[int, int]],
        explored: set[tuple[int, int]]
    ) -> None:
        self.path = path
        self.explored = explored


class NoSolution(Solution):
    pass
