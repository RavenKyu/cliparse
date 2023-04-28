from argparse import ArgumentParser
from . import run


################################################################################
def arg_parser():
    parser = ArgumentParser(
        prog='cliparse',
        description='CLI Framework with Argparse',
        epilog='For more information, see the documentation.',
    )
    parser.add_argument('cli_package', type=str,
                        help="Python scripts where the `argument_parser` function exists.")
    return parser


################################################################################
if __name__ == '__main__':
    arguments = arg_parser()
    arg_spec = arguments.parse_args()
    if not arg_spec.cli_package:
        exit(1)
    run(arg_spec.cli_package)
