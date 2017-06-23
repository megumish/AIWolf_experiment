from util.common import *
import glob, os

def init(__config):
    global __logs
    __logs = glob.glob(__config.input_dir + '/*')

    os.mkdir(__config.output_dir)
    os.mkdir(__config.output_image_dir)
    os.mkdir(__config.output_answer_dir)

    global filenum_role_map
    filenum_role_map = {k:v for k, v in zip(role.types, [0 for i in range(len(role.types))])}
