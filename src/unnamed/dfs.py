from .base import Frontier


class QueueFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop(0)
