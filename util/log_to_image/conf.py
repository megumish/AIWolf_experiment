import os
import logging

class Config:
    __logger = logging.getLogger(__name__)
    def __init__(self):
        self.__message_level = logging.WARNING
        self.__input_dir = ""
        self.__output_num = ""
        self.__output_dir = ""

    @property
    def message_level(self):
        return self.__message_level
    @message_level.setter
    def message_level(self, message_level):
        self.__message_level = message_level
        Config.__logger.setLevel(message_level)
        handler = logging.StreamHandler()
        handler.setLevel(message_level)
        Config.__logger.addHandler(handler)
        Config.__logger.debug("DEBUG MODE")

    @property
    def input_dir(self):
        return self.__input_dir
    @input_dir.setter
    def input_dir(self, directory):
        while directory[-1] == '/':
            del directory[-1]
        self.__input_dir = directory
        Config.__logger.debug('set INPUT DIRECTORY:%s' % (directory))
    @input_dir.getter
    def input_dir(self):
        return self.__input_dir

    @property
    def output_dir(self):
        return self.__output_dir
    @output_dir.setter
    def output_dir(self, directory):
        while directory[-1] == '/':
            del directory[-1]
        self.__output_dir = directory
        self.__output_answer_dir = self.__output_dir + '/ans'
        self.__output_image_dir = self.__output_dir + '/img'
        Config.__logger.debug('set OUTPUT DIRECTORY:%s' % (directory))
    @output_dir.getter
    def output_dir(self):
        return self.__output_dir

    @property
    def output_answer_dir(self):
        return None
    @output_answer_dir.getter
    def output_answer_dir(self):
        return self.__output_answer_dir

    @property
    def output_image_dir(self):
        return None
    @output_image_dir.getter
    def output_image_dir(self):
        return self.__output_image_dir
