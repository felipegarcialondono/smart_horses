from abc import ABC, abstractmethod

class Game(ABC):
    @abstractmethod
    def state_initial(self):
        pass

    @abstractmethod
    def operators(self, state):
        pass

    @abstractmethod
    def is_terminal(self, state):
        pass

    @abstractmethod
    def utility(self, state):
        pass
