from src.pathfinder.models.solution import Solution
from src.widgets import Label, Popup


class State:
    __instance = None
    
    overlay: bool = False
    label: Label
    speed_label: Label
    done_visualising: bool
    need_update: bool
    results: dict[str, dict[str, float]]
    run_all_mazes = False
    results_popup: Popup | None = None

    def __new__(cls):
        if State.__instance is None:
            State.__instance = object.__new__(cls)

        return State.__instance
