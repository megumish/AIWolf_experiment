import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.WARNING)
logger.setLevel(logging.WARNING)
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

class Convertable(Interchangeable):
    def __init__(self, types, type_argnum_map):
        for t in types:
            if not t in type_argnum_map.keys():
                logger.error("talk type_argnum_map.keys() does not match with talk type: %s" % (t))
                sys.exit()
        super().__init__(types)
        self.__str_head_map = {}
        head = 0
        for t, argnum in type_argnum_map.items():
            __str_head_map[t] = head
            head += argnum
        self.__head_str_map = {v:k for k, v in self.__str_head_map.items()}
    def str_to_head(self, _str):
        return self.__str_head_map[_str]
    def head_to_str(self, _index):
        return self.__head_str_map[_index]

role = Interchangeable(['WEREWOLF', 'POSSESSED', 'VILLAGER', 'BODYGUARD', 'MEDIUM', 'SEER'])

species = Interchangeable(['WEREWOLF', 'HUMAN'])

__action_types = ['TALK', 'VOTE']
__action_type_argnum_map = {'TALK':1, 'VOTE':1}
action = Convertable(__action_types, __action_type_argnum_map)

__vote_types = ['VOTE']
__vote_type_argnum_map = {'VOTE':1}
vote = Convertable(__vote_types, __vote_type_argnum_map)

__talk_types = ['ESTIMATE', 'COMINGOUT', 'DIVINATION', 'DIVINED', 'INQUESTED', 'GUARD', 'GUARDED', 'VOTE', 'ATTACK', 'AGREE', 'DISAGREE', 'OVER', 'SKIP', 'REQUEST']
__talk_type_argnum_map = {'ESTIMATE':2, 'COMINGOUT':2, 'DIVINATION':1, 'DIVINED':2, 'INQUESTED':2, 'GUARD':1, 'GUARDED':1, 'VOTE':1, 'ATTACK':1, 'AGREE':-1, 'DISAGREE':-1, 'OVER':0, 'SKIP':0, 'REQUEST':-1 }
# add number for subject.
__talk_type_argnum_map = {k:v for k, v in map(lambda ab: (ab[0], ab[1]+1), talk.type_argnum_map.items())}
talk = Convertable(__talk_types, __talk_type_argnum_map)

def role_to_species(role_str):
    if role.str_to_index(role_str) == 0:
        return 'WEREWOLF'
    else:
        return 'HUMAN'

def index_to_logindex_str(index):
    return ('%02d') % index
