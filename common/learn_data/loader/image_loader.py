import logging
import os
import numpy
from PIL import Image
from chainer import cuda
import glob
import common
from common.data import Data

class ImageLoader:
    def __init__(self, message_level=logging.WARNING, message_formatter=None):
        self.__logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        self.__logger.setLevel(message_level)
        handler.setLevel(message_level)
        if not message_formatter is None:
            handler.setFormatter(message_formatter)
        self.__logger.addHandler(handler)

    def load(self, config, is_test=False):
        if is_test:
            return self.__load_test_data(config)
        else:
            return self.__load_train_data(config)

    def __load_train_data(self, config):
        return self.__load_data(config)

    def __load_test_data(self, config):
        for role_type in common.role.types:
            self.__load_data(config, role_type=role_type)
        return data

    def __load_data(self, config, role_type=None):
        xp = numpy
        #if config.use_gpu:
        #    xp = cuda.cupy
        data = Data()
        data.answers = {}
        data.inputs = {}
        answers = []
        inputs = []
        if role_type is None:
            image_files = glob.glob(os.path.join(config.get_input_data_dir(), '*'))
        else:
            image_files = glob.glob(os.path.join(config.get_input_data_dir(), role_type, '*'))

        loaded_image_size = False
        for image_file in image_files:
            image = Image.open(image_file)
            if not loaded_image_size:
                data.image_size = image.size[0]
                loaded_image_size = True
            image_array = numpy.asarray(image).astype(xp.float32)
            image_array = image_array.ravel()
            image_array = image_array / 255.0
            inputs.append(image_array)
            image_name = os.path.basename(image_file)
            answer_name = os.path.join(config.get_input_answer_dir(), '_'.join(image_name.replace('.png', '').split('_')[:-1]))
            answer_file = open(answer_name, 'r')
            answers.append(answer_file.read())
            answer_file.close()
        self.__logger.debug('set answers%s' % (str(answers)))
        self.__logger.debug('set inputs%s' % (str(inputs)))
        data.answers[role_type] = answers
        data.inputs[role_type] = inputs
        return data
