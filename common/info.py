import common
import logging
from progressbar import ProgressBar, Percentage, Bar, Timer

class ConvertInfo:
    def __init__(self, message_level=logging.WARNING, message_formatter=None):
        self.__logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        self.__logger.setLevel(message_level)
        handler.setLevel(message_level)
        if not message_formatter is None:
            handler.setFormatter(message_formatter)
        self.__logger.addHandler(handler)

    def narrow_down_targets(self, log_row, game_setting):
        targets = set(self.targets)
        if self.choice != 'all':
            winner = log_rows[-1].split(',')[-1]
            winner_roles = set()
            for role in game_setting.player_roles:
                if role_to_species(role) == winner:
                    winner_roles.append(role)
            winners = set()
            for name, role in player_name_role_map.items():
                if role in winner_roles:
                    winners.append(name)
            if self.choice == 'winner':
                targets = self.targets.intersection(winners)
            elif self.choice == 'loser':
                targets = self.targets.difference(winners)
        return targets
    
    def init_progress(self):
        widgets = ['Total: ', Percentage(), ' ', Bar(), ' ', Timer()]
        maxval = self.output_num * len(common.role.types)
        self.__progress= ProgressBar(widgets=widgets, maxval=maxval)

    def update_progress(self):
        self.__progress.update(sum(self.role_filenum_map.values()))

class LearnInfo:
    def __init__(self, message_level=logging.WARNING, message_formatter=None):
        self.__logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        self.__logger.setLevel(message_level)
        handler.setLevel(message_level)
        if not message_formatter is None:
            handler.setFormatter(message_formatter)
        self.__logger.addHandler(handler)

class GameSetting:
    def __init__(self, log_rows):
        player_num = 0
        player_names = []
        player_roles = []
        for log_row in log_rows:
            if log_row.split(',')[1] != 'STATUS': break
            player_names.append(log_row.split(',')[-1])
            player_roles.append(log_row.split(',')[3])
            player_num += 1
        self.player_num = player_num
        self.player_names = player_names
        self.player_roles = player_roles
        self.day_num = int(log_rows[-1].split(',')[0])

class GameInfo:
    def __init__(self, gameSetting):
        self.talks = [[] for i in range(gameSetting.day_num + 1)]
        self.votes = [[] for i in range(gameSetting.day_num + 1)]
