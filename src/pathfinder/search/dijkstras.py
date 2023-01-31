from __future__ import annotations
import time
from typing import Optional


from ..types import Visualiser
from ..models.frontier import PriorityQueueFrontier
from ..models.node import Node, Node
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class DijkstrasSearch:
    @staticmethod
    def search(grid: Grid, callback: Optional[Visualiser] = None) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points
            callback (Optional[Visualiser], optional): Callback for 
            visualisation. Defaults to None.

        Returns:
            Solution: Solution found
        """
        start_time = time.time()

        # Create Node for the source cell
        node = grid.get_node(pos=grid.start)

        # Instantiate PriorityQueue frontier and add node into it
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        # Keep track of G scores
        distance = {grid.start: 0}

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution(
                    [], list(distance), (time.time() - start_time) * 1000
                )

            # Remove node from the frontier
            node = frontier.pop()

            # If reached destination point
            if node.state == grid.end:

                # Generate path and return a Solution object
                cells = []

                temp = node
                while temp.parent != None:
                    cells.append(temp.state)
                    temp = temp.parent

                cells.append(grid.start)
                cells.reverse()

                return Solution(
                    cells, list(distance), (time.time() - start_time) * 1000
                )

            # Call the visualiser function, if provided
            if node.parent and callback:
                callback(node.state, delay=True)

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
