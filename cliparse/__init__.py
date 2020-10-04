__version__ = '1.0.0b4'

import io
import cmd
import sys
import readline
import shlex
import traceback
import importlib.util

from argparse import _SubParsersAction
from argparse import _HelpAction, Action
from contextlib import redirect_stdout

# Prevent to execute exit() when help and error method in argparse.Argparser
sys.exit = lambda: None


################################################################################
class ArgumentCmd(cmd.Cmd):
    argument_parser = None

    # ==========================================================================
    def __init__(self):
        super(ArgumentCmd, self).__init__()
        readline.set_completer_delims(' ')
        ArgumentCmd.read_prompt()

    # ==========================================================================
    def _do_command(self, line, *args, **kwargs):
        parser = self.argument_parser
        prog = kwargs["prog"].strip()
        try:
            command = f'{prog} {line}'.strip()
            spec = parser.parse_args(shlex.split(command))
            if 'func' not in spec:
                return
            if any(x in command for x in ('-h', '--help')):
                return
            spec.func(spec)
        except TypeError:
            # parse_args raise exception when wrong input.
            return
        except Exception as e:
            traceback.print_exc()
            # Todo: Do something for errors
            return

    # ==========================================================================
    def emptyline(self):
        pass

    # ==========================================================================
    def postcmd(self, stop: bool, line: str) -> bool:
        ArgumentCmd.read_prompt()
        return cmd.Cmd.postcmd(self, stop, line)

    # ==========================================================================
    def complete(self, text, state):
        if state == 0:
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            command, args, foo = self.parseline(line)
            if command == '':
                result = self.completedefault
            else:
                result = ArgumentCmd.get_complete_list(
                    shlex.split(line), self.argument_parser)
                result = [x + ' ' for x in result]
            result.append(None)
            self.completion_matches = result
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    # ==========================================================================
    @staticmethod
    def get_complete_list(line, parser, result=None):
        if None is result:
            result = list()
        word = ''
        if line:
            word = line.pop(0)
        for action in parser._actions:
            if isinstance(action, _HelpAction):
                continue
            elif isinstance(action, _SubParsersAction):
                rc = [x for x in action.choices.keys() if x.startswith(word)]
                if 1 == len(rc) and word == rc[0]:
                    return ArgumentCmd.get_complete_list(
                        line, action.choices[word], list())
                result += [x for x in action.choices.keys() if x.startswith(word)]
            elif isinstance(action, Action):
                result += [x for x in action.option_strings if x.startswith(word)]
            else:
                pass
        return result

    # ==========================================================================
    @staticmethod
    def get_empty_func(_type, action, parser):
        def do(self, line):
            self._do_command(self, line, prog=action.prog)

        def complete(self, text, line, start_index, end_index):
            return self._complete_command(
                self, text, line, start_index, end_index)

        f = {'do': do, 'complete': complete}
        return f[_type]

    # ==========================================================================
    @classmethod
    def _add_functions(cls, actions, parser):
        for action in actions.choices.values():
            with io.StringIO() as buf, redirect_stdout(buf):
                print(action.print_usage())
                output = buf.getvalue()

            for _type in ('do',):
                command = ArgumentCmd.get_empty_func(
                    _type, action=action, parser=parser)
                command.__doc__ = output
                command.__name__ = f"{_type}_{action.prog.split()[-1].strip()}"
                setattr(cls, command.__name__, classmethod(command))

    # ==========================================================================
    @classmethod
    def _add_command(cls, parser):
        for action in parser._actions:
            if isinstance(action, _HelpAction):
                continue
            if isinstance(action, _SubParsersAction):
                ArgumentCmd._add_functions(action, parser)

    # ==========================================================================
    @classmethod
    def set_cli_parser(cls, parser):
        cls.argument_parser = parser
        cls._add_command(parser)

    # ==========================================================================
    @staticmethod
    def read_prompt():
        try:
            with open('prompt', 'r') as f:
                prompt = f.read()
                if prompt:
                    ArgumentCmd.prompt = prompt + ' '
        except FileNotFoundError:
            pass
        return ArgumentCmd.prompt

################################################################################
def run(cli_package):
    # Import user CLI package
    module_name = 'cli'
    spec = importlib.util.spec_from_file_location('cli', cli_package)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    cli_parser = module.argument_parser()

    # Run CLI-Arguments
    command = ArgumentCmd
    command.set_cli_parser(cli_parser)
    my_cmd = command()
    my_cmd.cmdloop()
