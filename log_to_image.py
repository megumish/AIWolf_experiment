from argparse import ArgumentParser
import logging
from util.log_to_image import conf, gen

__config = conf.Config()
def parse_args():
    global __config

    description = 'AIWolf log to image. By default, generate train mode image used all agent data'
    argparser = ArgumentParser(description=description)
    argparser.add_argument('input_dir', metavar='INPUT_DIR', type=str, help='input log file')
    argparser.add_argument('output_num', metavar='OUTPUT_NUM', type=int, help='number of outputs of each role')
    argparser.add_argument('-v', '--verbose', action='store_true', help='show verbose message')
    argparser.add_argument('-o', '--output', metavar='OUTPUT_DIR', dest='ouput_dir', help='output to a directory named <directory>')
    mode = argparser.add_mutually_exclusive_group()
    mode.add_argument('--train', metavar='AGENT_NAME', type=str, nargs='*', help='learn <AGENT_NAME>s')
    mode.add_argument('--test', metavar='AGENT_NAME', type=str, nargs='*', help='test <AGENT_NAME>s')
    mode.add_argument('--train_except', metavar='AGENT_NAME', type=str, nargs='*', help='train all agent except <AGENT_NAME>s')
    mode.add_argument('--test_except', metavar='AGENT_NAME', type=str, nargs='*', help='test all agent except <AGENT_NAME>s')

    args = argparser.parse_args()
    __config.input_dir = args.input_dir
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if hasattr(args, 'output_dir'):
        __config.output_dir = args.output_dir
    else:
        __config.output_dir = __config.input_dir + '_out'

if __name__ == "__main__":
    parse_args()
    gen.init(__config)
