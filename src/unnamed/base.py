class Node:
    def __init__(self, state, parent, action):
        self.state: tuple = state
        self.parent: Node = parent
        self.action: str = action


class Frontier:
    def __init__(self):
        self.frontier: list[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0
