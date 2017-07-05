import numpy
import logging
import common
from . import Evaluator

class RevealedEvaluator(Evaluator):
    def __init__(self, message_level=logging.WARNING, message_formatter=None):
        self.__logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        self.__logger.setLevel(message_level)
        handler.setLevel(message_level)
        if not message_formatter is None:
            handler.setFormatter(message_formatter)
        self.__logger.addHandler(handler)

        self.vector_size = 0
        for instance in common.action.type_instance_map.values():
            self.vector_size += instance.tail_num
    
    def evaluate(self, content, game_setting, game_info):
        if content.action_type == 'TALK':
            self.__logger.debug("evaluate TALK")
            return self.__evaluate_talk(content, game_setting, game_info)
        if content.action_type == 'VOTE':
            self.__logger.debug("evaluate VOTE")
            return self.__evaluate_vote(content, game_setting, game_info)
        return None

    def __evaluate_talk(self, content, game_setting, game_info):
        topic = content.argv[0]
        talk = common.action.type_instance_map['TALK']
        values = numpy.zeros(talk.type_argnum_map[topic])
        if topic in {'ESTIMATE', 'COMINGOUT'}:
            target_role = game_setting.player_roles[common.logindex_str_to_index(content.argv[1])]
            values[0] = common.role.str_to_index(target_role)
            values[1] = common.role.str_to_index(content.argv[2])
        if topic in {'DIVINATION', 'GUARD', 'VOTE', 'ATTACK', 'GUARDED'}:
            target_role = game_setting.player_roles[common.logindex_str_to_index(content.argv[1])]
            values[0] = common.role.str_to_index(target_role)
        if topic in {'DIVINED', 'INQEUSTED'}:
            target_role = game_setting.player_roles[common.logindex_str_to_index(content.argv[1])]
            values[0] = common.role.str_to_index(target_role)
            values[1] = common.species.str_to_index(content.argv[2])
        if topic == 'AGREE':
            pass    
        if topic == 'DISAGREE':
            pass
        if topic in {'OVER', 'SKIP'}:
            values = numpy.zeros(1)
            values[0] = 1
        index = talk.str_to_head(topic)
        return index, values

    def __evaluate_vote(self, content, game_setting, game_info):
        vote = common.action.type_instance_map['VOTE']
        talk = common.action.type_instance_map['TALK']
        index = talk.tail_num + vote.str_to_head('VOTE')
        target_role = game_setting.player_roles[common.logindex_str_to_index(content.argv[0])]
        return index, numpy.array([float(common.role.str_to_index(target_role))])
