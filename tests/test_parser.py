import unittest
from cliparse import CommandArgumentParser,  ArgumentCmd
from cliparse import _SubParsersAction, _HelpAction
import pprint


class MyTestCase(unittest.TestCase):
    @staticmethod
    def argument_parser():
        parser = CommandArgumentParser(
            prog='',
            description='description',
            epilog='end of description',)

        sub_parser = parser.add_subparsers(dest='sub_parser')
        init_parser = sub_parser.add_parser('init', help='Initialize database')
        init_parser.add_argument('-d', '--init-db', action='store_true',
                                 help='initialize database.')
        init_parser.add_argument('-m', '--dummy-members', action='store_true',
                                 help='insert dummy members.')
        init_parser.add_argument('-b', '--dummy-books', action='store_true',
                                 help='insert dummy books.')
        init_parser.add_argument('-r', '--dummy-rental', action='store_true',
                                 help='insert dummy rental.')

        init_subparser = init_parser.add_subparsers(dest='init_subparser', help='init_sub')
        init_sub = init_subparser.add_parser('book', help='About Book')
        init_sub.add_argument('-a', '--about', help='about sub')

        init_sub = init_subparser.add_parser('book2', help='About Book')
        init_sub.add_argument('-a', '--about', help='about sub')

        run_app = sub_parser.add_parser('server', help='Run api server')
        run_app.add_argument('-a', '--address', default='localhost',
                             help='host address')
        run_app.add_argument('-p', '--port', type=int, default=5000,
                             help='port')
        run_app.add_argument('-d', '--debug', action='store_true')

        return parser

    def setUp(self) -> None:
        self.parser = self.argument_parser()

    def test0010_parser(self):
        # add_command('a', parser=self.parser)
        pass

    def test0020_subparser(self):
        self.parser.parse_args('-h'.split())

    def test0100_get_complete_list(self):
        line = ''.split()
        parser = self.argument_parser()
        print(ArgumentCmd.get_complete_list(line, parser))


if __name__ == '__main__':
    unittest.main()
