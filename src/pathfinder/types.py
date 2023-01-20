from typing import Protocol


class Visualiser(Protocol):
    def __call__(
        self,
        coords: tuple[int, int],
        color: tuple[int, int, int] = (220, 235, 113),
        delay: bool = False
    ) -> None:
        pass
