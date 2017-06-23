from util.common import *
import glob, os, shutil
import sys
import logging
import functools

__logger = logging.getLogger(__name__)
__done_init = False
def init(config):
    global ____logger
    __logger.debug("init GENERATION MODULE")

    message_level = config.message_level
    handler = logging.StreamHandler()
    __logger.setLevel(message_level)
    handler.setLevel(message_level)
    __logger.addHandler(handler)

    global __is_dry_run
    global __output_dir
    __is_dry_run = config.is_dry_run
    __output_dir = config.output_dir
    __logger.debug("start DRY RUN")

    os.mkdir(config.output_dir)
    os.mkdir(config.output_image_dir)
    os.mkdir(config.output_answer_dir)
    __logger.debug("create OUTPUT DIRECTORIES:%s,%s,%s" % (config.output_dir, config.output_image_dir, config.output_answer_dir))

    global __filenum_role_map
    __filenum_role_map = {k:v for k, v in zip(role.types, [0 for i in range(len(role.types))])}
    __logger.debug("create FILENUM ROLE MAP")

    log_files = glob.glob(config.input_dir + "/*")
    global __logs
    __logs = []
    for log_file, num_of_file in zip(log_files, range(0, len(log_files))):
        __logs.append([])
        __logger.debug("open LOG FILE:%s" % (log_file))
        raw_log_data = open(log_file)
        raw_log_rows = raw_log_data.readlines()
        for raw_log_row in raw_log_rows:
            __logs[num_of_file].append(raw_log_row.strip().upper())
    __logger.debug("read LOG FILES")

    global __targets
    __targets = set()
    for log in __logs: 
        for row in log:
            if row.split(',')[1] != 'STATUS':
                break 
            __targets.add(row.split(',')[-1])
    if (config.include_players and config.except_players):
        __logger.error("set ON INCLUDE AND EXCEPT PLAYER")
        sys.exit()
    include_players = set(map(lambda s: s.upper(), config.include_players))
    except_players = set(map(lambda s: s.upper(), config.except_players))
    for player in include_players.difference(__targets):
        __logger.warning("PLAYER:%s isn't in %s" % (player, config.input_dir))
    if include_players:
        __targets = __targets.intersection(include_players)
    if except_players:
        __targets = __targets.difference(except_players)
    for target in __targets:
        __logger.debug("set TARGET PLAYER:%s" % (target))

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
def run():
    global __output_dir
    global __logger
    if __is_dry_run:
        shutil.rmtree(__output_dir)
