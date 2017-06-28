from common import *
from . import info
import glob, os, shutil
import sys
import logging
import functools
from PIL import Image

__logger = logging.getLogger(__name__)
__done_init = False
__info = info.ConvertInfo()
def init(config, message_level=logging.WARNING, message_formatter=None):
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

    # set output info
    __info.output_dir = config.get_output_dir()
    __info.output_num = config.get_output_num()
    os.mkdir(config.get_output_dir())
    os.mkdir(config.get_output_data_dir())
    os.mkdir(config.get_output_answer_dir())
    __logger.debug("create OUTPUT DIRECTORIES:%s,%s,%s" % (config.get_output_dir(), config.get_output_data_dir(), config.get_output_answer_dir()))

    # set role file num map
    __info.role_filenum_map = {k:v for k, v in zip(role.types, [0 for i in range(len(role.types))])}
    __logger.debug("create ROLE FILENUM MAP")

    # load raw log files
    log_files = glob.glob(config.get_input_dir() + "/*")
    __info.logs = []
    for log_file, num_of_file in zip(log_files, range(0, len(log_files))):
        __info.logs.append([])
        __logger.debug("open LOG FILE:%s" % (log_file))
        raw_log_data = open(log_file)
        raw_log_rows = raw_log_data.readlines()
        for raw_log_row in raw_log_rows:
            __info.logs[num_of_file].append(raw_log_row.strip().upper())
    __logger.debug("read LOG FILES")

    # set train/test targets
    __info.targets = set()
    for log in __info.logs: 
        for row in log:
            if row.split(',')[1] != 'STATUS':
                break 
            __info.targets.add(row.split(',')[-1])
    if (config.include_players and config.except_players):
        __logger.error("set ON INCLUDE AND EXCEPT PLAYER")
        sys.exit()
    include_players = set(map(lambda s: s.upper(), config.include_players))
    except_players = set(map(lambda s: s.upper(), config.except_players))
    for player in include_players.difference(__info.targets):
        __logger.warning("PLAYER:%s isn't in %s" % (player, config.input_dir))
    if include_players:
        __info.targets = __info.targets.intersection(include_players)
    if except_players:
        __info.targets = __info.targets.difference(except_players)
    for target in __info.targets:
        __logger.debug("set TARGET PLAYER:%s" % (target))

    # set train/test mode
    __info.mode = config.mode

    # set choice 
    __info.choice = config.choice

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

__data_num = 0
def __count_some_nums(func):
    global __data_num
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        __count_filenum(*args, **kwargs)
        __data_num += 1
    return wrapper

def __count_filenum(role_str=None):
    global __logger
    if not role_str:
        __logger.error("CAN'T COUNT None ROLE")
        sys.exit()
    global __role_filenum_map
    __role_filenum_map[role_str] += 1

@__enable_to
def run(converter):
    global __logger

    __logger.debug("start to convert")
    converter.convert(__info)
    __logger.debug("finished to convert")
