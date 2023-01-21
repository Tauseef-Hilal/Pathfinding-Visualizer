from __future__ import annotations


class Node:
    def __init__(
        self,
        state: tuple[int, int],
        parent: Node | None,
        action: str | None
    ) -> None:
        self.state = state
        self.parent = parent
        self.action = action

    def __repr__(self) -> str:
        return f"Node({self.state!r}, Node(...), {self.action!r})"


class AStarNode(Node):
    def __init__(
        self,
        state: tuple[int, int],
        parent: AStarNode | None,
        action: str | None,
        distance_from_start: int
    ) -> None:

        super().__init__(state, parent, action)
        self.distance_from_start = distance_from_start

    def __lt__(self, other: AStarNode):
        return self.state < other.state
