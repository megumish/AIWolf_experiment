import logging
import sys

logger = getLogger(__name__)
handler = StreamHandler()
logger.addHandler(handler)

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
talk.type_argnum_map = {'ESTIMATE':2, 'COMINGOUT':2, 'DIVINATION':1, 'DIVINED':2, 'INQUESTED':2, 'GUARD':1, 'GUARDED':1, 'VOTE':1, 'ATTACK':1, 'AGREE':-1, 'DISAGREE':-1, 'OVER':0, 'SKIP':0, 'REQUEST':-1 }
# add number for subject.
talk.type_argnum_map = {k:v for k, v in map(lambda (a, b): return (a, b+1), type_argnum_map.itemes())}

action = Interchangeable(['VOTE'])
action.type_argnum_map = {'VOTE':1}
# add number for subject.
action.type_argnum_map = {k:v for k, v in map(lambda (a, b): return (a, b+1), type_argnum_map.itemes())}

# check
for t in talk.type:
    if not t in talk.type_argnum_map.keys():
        logger.error("talk type_argnum_map.keys() does not match with talk type: %s", % (t))
        sys.exit()
for t in action.type:
    if not t in action.type_argnum_map.keys():
        logger.error("action type_argnum_map.keys() does not match with action type: %s", % (t))
        sys.exit()

def role_to_species(role_str):
    if role.str_to_index(role_str) == 0:
        return 'WEREWOLF'
    else:
        return 'HUMAN'

def index_to_logindex_str(index):
    return ('%02d') % index
