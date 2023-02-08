from __future__ import annotations


class Node:
    def __init__(
        self,
        value: str,
        state: tuple[int, int],
        cost: int,
        parent: Node | None = None,
        action: str | None = None
    ) -> None:
        self.value = value
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        self.estimated_distance = float("inf")

    def __lt__(self, other: Node) -> bool:
        if self.estimated_distance == float("inf"):
            return self.state < other.state
        
        return self.estimated_distance < other.estimated_distance

    def __repr__(self) -> str:
        return f"Node({self.state!r}, Node(...), {self.action!r})"
