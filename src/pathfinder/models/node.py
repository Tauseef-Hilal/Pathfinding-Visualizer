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
    
    def __lt__(self, other: Node) -> bool:
        return self.state < other.state

    def __repr__(self) -> str:
        return f"Node({self.state!r}, Node(...), {self.action!r})"
