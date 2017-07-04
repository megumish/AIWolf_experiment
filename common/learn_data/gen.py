import common
import glob, os, shutil
import sys
import logging
import functools

__logger = logging.getLogger(__name__)
__done_init = False
__info = common.info.LearnInfo()
def init(config, loader, message_level=logging.WARNING, message_formatter=None):
    # set logger
    global __logger
    handler = logging.StreamHandler()
    __logger.setLevel(message_level)
    handler.setLevel(message_level)
    if not message_formatter is None:
        handler.setFormatter(message_formatter)
    __logger.addHandler(handler)

    __logger.debug("init GENERATION MODULE")
    
    # set run info
    __info.is_dry_run = config.is_dry_run
    __logger.debug("start DRY RUN")

    __info.epoch_num = config.epoch_num
    __info.batch_size = config.batch_size

    # set output info
    __info.output_model = config.get_output_model()
    parent_dirs = os.path.dirname(__info.output_model)
    if parent_dirs != '' and not os.path.isdir(parent_dirs):
        os.mkdirs(parent_dirs)
        __logger.debug("create OUTPUT DIRS:%s" % (parent_dirs))

    # use GPU?
    __info.use_gpu = config.use_gpu

    # load data
    __info.data = loader.load(config)

    # set train/test mode
    __info.mode = config.mode

    global __done_init
    __done_init = True

def __enable_to(func):
    global __logger
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not __done_init:
            __logger.error("call %s.init() before this function" % (__name__))
            sys.exit()
        else:
            func(*args, **kwargs)
    return wrapper

@__enable_to
def run(learner):
    global __logger
    global __info

    __logger.debug("start to convert")
    learner.build(__info)
    #__info.init_progress()
    if __info.mode == 'test':
        learner.test(__info)
    else:
        learner.train(__info)
    __logger.debug("finished to convert")
