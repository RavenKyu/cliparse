__version__ = '1.0.0b0'

import cmd
import sys
import readline
import shlex
from argparse import ArgumentParser
from argparse import _SubParsersAction
from argparse import _HelpAction

import io
from contextlib import redirect_stdout
import traceback


################################################################################
class CommandArgumentParser(ArgumentParser):
    # Preventing to execute exit command after help or error
    def error(self, message):
        self.print_help(sys.stderr)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)


################################################################################
class ArgumentCmd(cmd.Cmd):
    argument_parser = None

    # ==========================================================================
    def __init__(self):
        super(ArgumentCmd, self).__init__()
        readline.set_completer_delims(' ')

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
    def _complete_command(self, text, line, start_index, end_index, **kwargs):
        parser = self.argument_parser()
        return ArgumentCmd.get_complete_list(line, parser).append(None)

    # ==========================================================================
    def emptyline(self):
        pass

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
            if isinstance(action, _SubParsersAction):
                if not word:
                    return [x for x in action.choices.keys()]
                rc = [x for x in action.choices.keys() if x.startswith(word)]
                if word not in rc:
                    return rc
                return ArgumentCmd.get_complete_list(
                    line, action.choices[word], list())

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
