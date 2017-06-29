import os, sys
import logging
import common

class Config:
    __logger = logging.getLogger(__name__)
    def __init__(self):
        self.__input_dir = ""
        self.__input_ans_dir = ""
        self.__input_data_dir = ""
        self.__model_name = ""

    def set_message_level_and_formatter(self, message_level, message_formatter=None):
        Config.__logger.setLevel(message_level)
        handler = logging.StreamHandler()
        handler.setLevel(message_level)
        if not message_formatter is None:
            handler.setFormatter(message_formatter)
        Config.__logger.addHandler(handler)
        Config.__logger.debug("set config DEBUG MODE")

    def set_input_dirs(self, directory):
        while directory[-1] == '/':
            del directory[-1]
        self.__input_dir = directory
        self.__input_answer_dir = self.__input_dir + '/ans'
        self.__input_data_dir = self.__input_dir + '/data'
        Config.__logger.debug('set INPUT DIRECTORY:%s' % (directory))
    def get_input_dir(self):
        return self.__input_dir
    def get_input_data_dir(self):
        return self.__input_data_dir
    def get_input_answer_dir(self):
        return self.__input_answer_dir

    def set_output_model(self, model_name):
        while model_name[-1] == '/':
            del model_name[-1]
        self.__output_model = model_name
        Config.__logger.debug('set OUTPUT MODEL:%s' % (model_name))
    def get_output_model(self):
        return self.__output_model
