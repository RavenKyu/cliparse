import sys
import importlib.util
from argparse import ArgumentParser

from . import ArgumentCmd


################################################################################
def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('cli_package', type=str)
    return parser


################################################################################
def run(cli_package):
    # Import user CLI package
    module_name = 'cli'
    spec = importlib.util.spec_from_file_location('cli', arg_spec.cli_package)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    cli_parser = module.argument_parser()

    # Run CLI-Arguments
    cmd = ArgumentCmd
    cmd.set_cli_parser(cli_parser)
    my_cmd = cmd()
    my_cmd.cmdloop()


################################################################################
if __name__ == '__main__':
    arguments = arg_parser()
    arg_spec = arguments.parse_args()
    run(arg_spec.cli_package)



