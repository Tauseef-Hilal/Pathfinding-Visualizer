from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class DijkstrasSearch:
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
        frontier.add(node)

        # Keep track of G scores
        distance = {grid.start: 0}

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
                cost = distance[node.state] + grid.get_cost(state)

                if state not in distance or cost < distance[state]:
                    distance[state] = cost

                    n = grid.get_node(pos=state)
                    n.parent = node

                    if not n.action:
                        n.action = action

                    frontier.add(
                        node=n,
                        priority=cost
                    )
