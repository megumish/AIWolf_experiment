from abc import ABCMeta, abstractmethod
from . import talk

class ABConverter(metaclass=ABCMeta):
    @abstractmethod
    def convert(self, info):
        pass

    @abstractmethod
    def __update_game_info(self, log_row):
        if log_row.split(',')[1] == 'TALK':
