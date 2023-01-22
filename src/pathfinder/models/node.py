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
    
    def __lt__(self, other: Node) -> bool:
        return self.state < other.state

    def __repr__(self) -> str:
        return f"Node({self.state!r}, Node(...), {self.action!r})"
