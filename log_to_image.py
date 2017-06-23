role_str_index_map = { 'WEREWOLF':1, 'POSSESSED':2, 'VILLAGER':3, 'BODYGUARD':4, 'MEDIUM':5, 'SEER':6 }
def role_str_to_index(role_str):
    return role_str_index_map[role_str]
role_index_str_map = {v:k for k, v in role_str_index_map.items()}
def role_index_to_str(role_index):
    return role_index_str_map[role_index]

talk_str_index_map = { 'ESTIMATE':0, 'COMINGOUT':1, 'DIVINATION':2, 'DIVINED':3, 'INQUESTED':4, 'GUARD':5, 'GUARDED': 6, 'VOTE':7, 'ATTACK':8, 'AGREE':8, 'DISAGREE':10, 'OVER':11, 'SKIP':12, 'OPERATOR': 13 }
def talk_str_to_index(talk_str):
    return talk_str_index_map[talk_str]
talk_index_str_map = {v:k for k, v in talk_str_index_map.items()}
def talk_index_to_str(talk_index):
    return talk_index_str_map[talk_index]
