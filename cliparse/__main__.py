from argparse import ArgumentParser
from . import run


################################################################################
def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('cli_package', type=str)
    return parser


################################################################################
if __name__ == '__main__':
    arguments = arg_parser()
    arg_spec = arguments.parse_args()
    run(arg_spec.cli_package)



