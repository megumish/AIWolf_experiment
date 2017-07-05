import common
class Content:
    def __init__(self, log_row, game_setting):
        self.action_type = log_row.split(',')[1]
        action_str = log_row.split(',')[-1]
        self.day = int(log_row.split(',')[0])
        if common.action.has_id[self.action_type]:
            self.id = int(log_row.split(',')[2])
        self.subject = common.logindex_str_to_index(log_row.split(',')[-2])
        self.argv = []
        for arg in action_str.split(' '):
            self.argv.append(arg.replace('AGENT[', '').replace(']', ''))
