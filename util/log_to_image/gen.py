from util.common import *
import glob, os, shutil
import sys
import logging
import functools
from PIL import Image

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

    global __output_num
    __output_num = config.output_num

    os.mkdir(config.output_dir)
    os.mkdir(config.output_image_dir)
    os.mkdir(config.output_answer_dir)
    __logger.debug("create OUTPUT DIRECTORIES:%s,%s,%s" % (config.output_dir, config.output_image_dir, config.output_answer_dir))

    global __role_filenum_map
    __role_filenum_map = {k:v for k, v in zip(role.types, [0 for i in range(len(role.types))])}
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

    global __mode
    __mode = config.mode

    global __choice
    __choice = config.choice

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
def run():
    global __logger

    global __mode
    __logger.debug("start to generate %s data" % (__mode))

    for log_rows in __logs:
        __log_rows_to_data(log_rows)
    
    __logger.debug("end to generate %s data" % (__mode))
    global __output_dir
    if __is_dry_run:
        shutil.rmtree(__output_dir)

def __log_rows_to_data(log_rows):
    player_num = 0
    player_names = []
    player_roles = []
    player_name_role_map = {}
    for log_row in log_rows:
        if log_row.split(',')[1] != 'STATUS': break
        player_names.append(log_row.split(',')[-1])
        player_roles.append(log_row.split(',')[3])
        player_name_role_map[log_row.split(',')[-1]] = log_row.split(',')[3]
        player_num += 1
    
    targets = __choice_targets(log_rows, player_roles, player_names)
    for index, name in zip(range(0, len(player_names)), player_names):
        if not name in targets: continue
        for log_row in log_rows:
            __log_row_to_data(log_row, player_names, player_roles)

def __choice_targets(log_rows, player_roles, player_names):
    global __targets
    targets = __targets
    global __choice
    if __choice != 'all':
        winner = log_rows[-1][-1]
        winner_roles = set()
        for role in player_roles:
            if role_to_species(role) == winner:
                winner_roles.append(role)
        winners = set()
        for name, role in player_name_role_map.items():
            if role in winner_roles:
                winners.append(name)
        if __choice == 'winner':
            targets = __targets.intersection(winners)
        elif __choice == 'loser':
            targets = __targets.difference(winners)
    return targets

def __log_row_to_data(log_row, player_names, player_roles):
    log_type = log_row.split(',')[1]
    if log_type == 'TALK':
        __talk_to_data(log_row, player_names, player_roles)

def __talk_to_data(log_row, player_names, player_roles):
    content = log_row.split(',')[-1]
    content_type = content.split(' ')[0]

