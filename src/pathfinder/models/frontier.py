from .node import Node


class Frontier:
    def __init__(self) -> None:
        self.frontier: list[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def contains_state(self, state: tuple[int, int]):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0
