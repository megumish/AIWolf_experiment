from abc import ABCMeta, abstractmethod

class Evaluator(metaclass=ABCMeta):
    @abstractmethod
    def evaluate(self, row, game_setting, game_info):
        pass

from . import simple
