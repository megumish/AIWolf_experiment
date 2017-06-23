class Config:
    def __init__(self):
        self.__input_dir = ""
        self.__output_num = ""
        self.__output_dir = ""

    @property
    def input_dir(self):
        return self.__input_dir

    @input_dir.setter
    def input_dir(self, directory):
        while directory[-1] == '/':
            del directory[-1]
        self.__input_dir = directory

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
