from __future__ import annotations
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
        # Create Node for the source cell
        node = Node(state=grid.start, parent=None, action=None)

        # Instantiate PriorityQueue frontier and add node into it
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        # Keep track of G scores
        distance = {grid.start: 0}

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution([], set(distance))

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

                return Solution(cells, set(distance))

            # Call the visualiser function, if provided
            if node.parent and callback:
                callback(node.state, delay=True)

            # Determine possible actions
            for action, state in grid.get_neighbours(node.state).items():
                cost = distance[node.state] + 1

                if state not in distance or cost < distance[state]:
                    distance[state] = cost

                    n = frontier.get(state)
                    n.parent = node

                    if not n.action:
                        n.action = action

                    frontier.add(
                        node=n,
                        priority=cost
                    )
