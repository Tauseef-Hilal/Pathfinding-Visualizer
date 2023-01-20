from typing import Optional

from ..types import Visualiser
from ..models.node import Node
from ..models.grid import Grid
from ..models.frontier import Frontier
from ..models.solution import NoSolution, Solution


class QueueFrontier(Frontier):
    def remove(self) -> Node:
        """Remove element from the queue

        Raises:
            Exception: Empty Frontier

        Returns:
            Node: Cell (Node) in a matrix
        """
        if self.is_empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop(0)


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid, callback: Optional[Visualiser] = None) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            callback (Optional[Visualiser], optional): Callback for 
            visualisation. Defaults to None.

        Returns:
            Solution: Solution found
        """

        # Create Node for the source cell
        node = Node(state=grid.start, parent=None, action=None)
        print(node)
        print(grid)

        # Instantiate Frontier and add node into it
        frontier = QueueFrontier()
        frontier.add(node)

        # Keep track of explored positions
        explored_states = set()

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution([], set())

            # Call the visualiser function, if provider
            if node.parent and callback:
                callback(node.state, delay=True)

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

                print(frontier)
                print(Solution(cells, explored_states))
                return Solution(cells, explored_states)

            # Add current node position the explored set
            explored_states.add(node.state)

            # Determine possible actions
            for action, state in grid.get_neighbours(node.state).items():
                new = Node(
                    state=state,
                    parent=node,
                    action=action
                )

                if state in explored_states or frontier.contains_state(state):
                    continue

                frontier.add(node=new)
