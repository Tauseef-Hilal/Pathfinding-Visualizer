from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points
            callback (Optional[Visualiser], optional): Callback for 
            visualisation. Defaults to None.

        Returns:
            Solution: Solution found
        """
        # Create Node for the source cell
        node = grid.get_node(pos=grid.start)

        # Instantiate PriorityQueue frontier and add node into it
        frontier = PriorityQueueFrontier()
        frontier.add(
            node,
            priority=AStarSearch.heuristic(grid.start, grid.end)
        )

        # Keep track of G scores
        g_score = {grid.start: 0}
        f_score = {grid.start: AStarSearch.heuristic(grid.start, grid.end)}

        # Keep track of explored nodes
        explored = []

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution([], explored)

            # Remove node from the frontier
            node = frontier.pop()
            if node.state not in explored:
                explored.append(node.state)

            # If reached destination point
            if node.state == grid.end:

                # Generate path and return a Solution object
                cells = []
                path_cost = 0

                temp = node
                while temp.parent != None:
                    cells.append(temp.state)
                    path_cost += temp.cost
                    temp = temp.parent

                cells.append(grid.start)
                cells.reverse()

                return Solution(cells, explored, path_cost=path_cost)

            # Determine possible actions
            for action, state in grid.get_neighbours(node.state).items():
                cost = g_score[node.state] + grid.get_cost(state)

                if state not in g_score or cost < g_score[state]:
                    g_score[state] = cost
                    f_score[state] = cost + \
                        AStarSearch.heuristic(state, grid.end)

                    n = grid.get_node(pos=state)
                    n.parent = node
                    n.estimated_distance = f_score[state] - cost

                    if not n.action:
                        n.action = action

                    frontier.add(
                        node=n,
                        priority=f_score[state]
                    )

    @staticmethod
    def heuristic(state: tuple[int, int], goal: tuple[int, int]) -> int:
        """Heuristic function for edtimating remaining distance

        Args:
            state (tuple[int, int]): Initial
            goal (tuple[int, int]): Final

        Returns:
            int: Distance
        """
        x1, y1 = state
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)
