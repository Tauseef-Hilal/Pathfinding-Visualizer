from src.pathfinder.models.solution import Solution
from src.widgets import Label


class State:
    __instance = None
    
    label: Label
    speed_label: Label
    done_visualising: bool
    need_update: bool
    results: dict[str, dict[str, float]]
    run_all_mazes = False

    def __new__(cls):
        if State.__instance is None:
            State.__instance = object.__new__(cls)

        return State.__instance
