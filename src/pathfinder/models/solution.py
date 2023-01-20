class Solution:
    def __init__(self, path: list[tuple[int, int]], runs: int) -> None:
        self.path = path
        self.runs = runs

class NoSolution(Solution):
    pass