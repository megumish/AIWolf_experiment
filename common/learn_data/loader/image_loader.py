import logging
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
        answer_files = glob.glob('%s/*' % (config.get_input_answer_dir()))
        if role_type is None:
            image_files = glob.glob('%s/*' % (config.get_input_data_dir()))
        else:
            image_files = glob.glob('%s/%s/*' % (config.get_input_data_dir(), role_type))

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
            image_name = image_file
            if '/' in image_file:
                image_name = image_file.split('/')[-1]
                image_answer_name = '_'.join(image_name.split('_')[:-1])
            for answer_file in answer_files:
                answer_name = answer_file
                if '/' in answer_name:
                    answer_name = answer_file.split('/')[-1]
                if answer_name == image_answer_name:
                    answer = open(answer_file)
                    answers.append(float(answer.read()))
                    answer.close()
                    break
        data.answers[role_type] = answers
        data.inputs[role_type] = inputs
        return data
