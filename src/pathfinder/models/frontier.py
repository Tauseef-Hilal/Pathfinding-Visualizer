from heapq import heappush, heappop

from .node import Node


class Frontier:
    """Model a frontier for managing nodes"""

    def __init__(self) -> None:
        self.frontier: list[Node] = []

    def add(self, node: Node) -> None:
        """Add a new node to the frontier

        Args:
            node (Node): Maze node
        """
        self.frontier.append(node)

    def contains_state(self, state: tuple[int, int]) -> bool:
        """Check if a state exists in the frontier

        Args:
            state (tuple[int, int]): Postion of a node

        Returns:
            bool: Whether the provided state exists
        """
        return any(node.state == state for node in self.frontier)

    def is_empty(self) -> bool:
        """Check if the frontier is empty

        Returns:
            bool: Whether the frontier is empty
        """
        return len(self.frontier) == 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} => {self.frontier}"


class StackFrontier(Frontier):
    def remove(self) -> Node:
        """Remove element from the stack

        Raises:
            Exception: Empty Frontier

        Returns:
            Node: Cell (Node) in a matrix
        """
        if self.is_empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop()


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


class PriorityQueueFrontier(Frontier):
    def __init__(self):
        self.frontier: list[tuple[int, Node]] = []

    def add(self, node: Node, priority: int = 0) -> None:
        """Add a new node into the frontier

        Args:
            node (AStarNode): Maze node
            priority (int, optional): Node priority. Defaults to 0.
        """
        heappush(self.frontier, (priority, node))

    def get(self, state: tuple[int, int]) -> Node | None:
        """Get node by state. Create new if not found

        Args:
            state (tuple[int, int]): State

        Returns:
            Node: Required node
        """
        for _, node in self.frontier:
            if node.state == state:
                return node

        return None

    def pop(self) -> Node:
        """Remove a node from the frontier

        Returns:
            AStarNode: Node to be removed
        """
        _, node = heappop(self.frontier)
        return node
