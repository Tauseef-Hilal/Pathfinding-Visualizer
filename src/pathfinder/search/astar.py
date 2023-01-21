from __future__ import annotations
from typing import Optional


from ..types import Visualiser
from ..models.frontier import PriorityQueueFrontier
from ..models.node import AStarNode
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class AStarSearch:
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
        node = AStarNode(state=grid.start, parent=None,
                         action=None, distance_from_start=0)

        # Instantiate PriorityQueue frontier and add node into it
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        # Keep track of explored positions
        explored_states = set()

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution([], explored_states)

            # Call the visualiser function, if provided
            if node.parent and callback:
                callback(node.state, delay=True)

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

                return Solution(cells, explored_states)

            # Add current node position into the explored set
            explored_states.add(node.state)

            # Determine possible actions
            for action, state in grid.get_neighbours(node.state).items():
                new = AStarNode(
                    state=state,
                    parent=node,
                    action=action,
                    distance_from_start=node.distance_from_start + 1
                )

                if state in explored_states or frontier.contains_state(state):
                    continue

                frontier.add(
                    new,
                    priority=new.distance_from_start +
                    AStarSearch.heuristic(state, grid.end)
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
        row, col = state
        goal_row, goal_col = goal

        return max(abs(goal_row - row), abs(goal_col - col))
