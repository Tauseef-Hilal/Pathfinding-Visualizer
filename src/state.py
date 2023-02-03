from src.widgets import Label


class State:
    __instance = None
    
    label: Label
    speed_label: Label
    done_visualising: bool
    need_update: bool

    def __new__(cls):
        if State.__instance is None:
            State.__instance = object.__new__(cls)

        return State.__instance
