class Grid:
    def __init__(
        self,
        grid: list[list[str]],
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> None:
        self.grid = grid
        self.start = start
        self.end = end

        # Calculate grid dimensions
        self.width = max(len(row) for row in grid)
        self.height = len(grid)
    
    def get_neighbours(
            self,
            pos: tuple[int, int]
    ) -> dict[str, tuple[int, int]]:
        """Determine the neighbours of a cell

        Args:
            pos (tuple[int, int]): Cell position

        Returns:
            dict[str, tuple[int, int]]: Action - Position Mapper
        """

        row, col = pos

        # Map actions with resulting cell positions
        action_pos_mapper = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1),
        }

        # Determine possilbe actions
        possible_actions = {}

        for action, (r, c) in action_pos_mapper.items():
            if not (0 <= r < self.height and 0 <= c < self.width):
                continue

            if self.grid[r][c] == "#":
                continue

            possible_actions[action] = (r, c)

        return possible_actions

    def __repr__(self) -> str:
        return f"Grid([[...], ...], {self.start}, {self.end})"
