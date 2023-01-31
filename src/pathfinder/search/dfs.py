from typing import Optional

from ..types import Visualiser
from ..models.node import Node
from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            callback (Optional[Visualiser], optional): Callback for 
            visualisation. Defaults to None.

        Returns:
            Solution: Solution found
        """

        # Create Node for the source cell
        node = grid.get_node(pos=grid.start)

        # Instantiate Frontier and add node into it
        frontier = StackFrontier()
        frontier.add(node)

        # Keep track of explored positions
        explored_states = {}

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution([], list(explored_states))

            # Remove node from the frontier
            node = frontier.remove()

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

                return Solution(cells, list(explored_states))

            # Add current node position the explored set
            explored_states[node.state] = True

            # Determine possible actions
            for action, state in grid.get_neighbours(node.state).items():
                if state in explored_states or frontier.contains_state(state):
                    continue

                new = grid.get_node(pos=state)
                new.parent = node
                new.action = action

                frontier.add(node=new)
