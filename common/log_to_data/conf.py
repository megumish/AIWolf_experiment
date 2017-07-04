import os, sys
import logging
import common

class Config:
    __logger = logging.getLogger(__name__)
    def __init__(self):
        self.__input_dir = ""
        self.__output_num = 0
        self.__output_dir = ""
        self.__output_ans_dir = ""
        self.__output_data_dir = ""

    def set_message_level_and_formatter(self, message_level, message_formatter=None):
        Config.__logger.setLevel(message_level)
        handler = logging.StreamHandler()
        handler.setLevel(message_level)
        if not message_formatter is None:
            handler.setFormatter(message_formatter)
        Config.__logger.addHandler(handler)
        Config.__logger.debug("set config DEBUG MODE")

    def set_input_dir(self, directory):
        directory = os.path.normpath(directory)
        self.__input_dir = directory
        Config.__logger.debug('set INPUT DIRECTORY:%s' % (directory))
    def get_input_dir(self):
        return self.__input_dir

    def set_output_num(self, num):
        if num < 0:
            Config.__logger.error('OUTPUT_NUM should be larger than 0')
            sys.exit()
        self.__output_num = num
    def get_output_num(self):
        return self.__output_num

    def set_output_dirs(self, directory):
        directory = os.path.normpath(directory)
        self.__output_dir = directory
        self.__output_answer_dir = os.path.join(self.__output_dir, 'ans')
        self.__output_data_dir = os.path.join(self.__output_dir, 'data')
        Config.__logger.debug('set OUTPUT DIRECTORY:%s' % (directory))
    def get_output_dir(self):
        return self.__output_dir
    def get_output_data_dir(self):
        return self.__output_data_dir
    def get_output_answer_dir(self):
        return self.__output_answer_dir
