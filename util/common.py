from argparse import ArgumentParser

class Interchangeable:
    def __init__(self, types):
        self.types = types
        self.__str_index_map = {k:v for k, v in zip(types, range(0, len(types)))}
        self.__index_str_map = {v:k for k, v in self.__str_index_map.items()}
    def str_to_index(self, _str):
        return self.__str_index_map[_str]
    def index_to_str(self, _index):
        return self.__index_str_map[_index]

role = Interchangeable(['WEREWOLF', 'POSSESSED', 'VILLAGER', 'BODYGUARD', 'MEDIUM', 'SEER'])

species = Interchangeable(['WEREWOLF', 'HUMAN'])

talk = Interchangeable(['ESTIMATE', 'COMINGOUT', 'DIVINATION', 'DIVINED', 'INQUESTED', 'GUARD', 'GUARDED', 'VOTE', 'ATTACK', 'AGREE', 'DISAGREE', 'OVER', 'SKIP', 'OPERATOR'])

action = Interchangeable(['VOTE'])

def get_image_size():
    return len(talk.types()) + len(action.types())

def role_to_species(role_str):
    if role.str_to_index(role_str) == 0:
        return 'WEREWOLF'
    else:
        return 'HUMAN'
