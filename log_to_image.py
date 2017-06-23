from argparse import ArgumentParser

class Role:
    __role_str_index_map = { 'WEREWOLF':0, 'POSSESSED':1, 'VILLAGER':2, 'BODYGUARD':3, 'MEDIUM':4, 'SEER':5 }
    def str_to_index(role_str):
        return __role_str_index_map[role_str]
    __role_index_str_map = {v:k for k, v in __role_str_index_map.items()}
    def index_to_str(role_index):
        return __role_index_str_map[role_index]

class Talk:
    __talk_str_index_map = { 'ESTIMATE':0, 'COMINGOUT':1, 'DIVINATION':2, 'DIVINED':3, 'INQUESTED':4, 'GUARD':5, 'GUARDED': 6, 'VOTE':7, 'ATTACK':8, 'AGREE':8, 'DISAGREE':10, 'OVER':11, 'SKIP':12, 'OPERATOR': 13 }
    talk_num = len(__talk_str_index_map)
    def str_to_index(talk_str):
        return __talk_str_index_map[talk_str]
    __talk_index_str_map = {v:k for k, v in __talk_str_index_map.items()}
    def index_to_str(talk_index):
        return __talk_index_str_map[talk_index]

__input_dir = ""
__player_num = 15
__output_num = 1000
__verbose = False
def parse_argv():
    usage = 'Usage: python3 {} INPUT_DIR OUTPUT_NUM [--verbose] [--output <directory>] [--help]'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('INPUT_DIR', type=str, help='input log file')
    argparser.add_argument('OUTPUT_NUM', type=int, help='number of outputs of each role')
    argparser.add_argument('-v', '--verbose', action='store_true', help='show verbose message')
    argparser.add_argument('-o', '--output', dest='ouput_directory', help='output to a directory named <directory>')

    args = argparser.parse_args()
    __input_dir = args.INPUT_DIR;
    __output_num = args.OUTPUT_NUM;
    __verbose = args.verbose;

if __name__ == "__main__":
    parse_argv()
