from __future__ import annotations


class Node:
    def __init__(
        self, state: tuple[int, int], parent: Node | None, action: str | None
    ) -> None:
        self.state = state
        self.parent = parent
        self.action = action
