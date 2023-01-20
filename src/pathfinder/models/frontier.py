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
