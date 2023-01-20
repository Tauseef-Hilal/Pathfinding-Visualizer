from typing import Optional

from ..types import Visualiser
from ..models.node import Node
from ..models.grid import Grid
from ..models.frontier import Frontier
from ..models.solution import NoSolution, Solution


class QueueFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop(0)


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid, callback: Optional[Visualiser] = None) -> Solution:
        node = Node(state=grid.start, parent=None, action=None)

        frontier = QueueFrontier()
        frontier.add(node)

        explored_states = set()

        ctr = 0
        while True:
            if frontier.empty():
                return NoSolution([], set())

            if node.parent and callback:
                callback(node.state, delay=True)

            node = frontier.remove()
            ctr += 1

            if node.state == grid.end:
                cells = []
                temp = node
                while temp.parent != None:
                    cells.append(temp.state)
                    temp = temp.parent
                cells.append(grid.start)
                cells.reverse()
                return Solution(cells, explored_states)

            explored_states.add(node.state)

            for action, state in grid.get_neighbours(node.state).items():
                new = Node(
                    state=state,
                    parent=node,
                    action=action
                )

                if state in explored_states or frontier.contains_state(state):
                    continue
                frontier.add(node=new)
