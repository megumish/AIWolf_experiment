import common

class BaseConverter:
    def _init_game_info(self, game_setting):
       self.game_info = common.info.GameInfo(game_setting) 

    def _update_game_info(self, content):
        if content.action_type == 'TALK':
            self.game_info.talks[content.day] = content
        if content.action_type == 'VOTE':
            self.game_info.votes[content.day] = content
