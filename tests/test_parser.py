import unittest
from sample_cli.cli import argument_parser
from cliparse import ArgumentCmd


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = argument_parser()

    def test00100_get_complete_list_auto_complete(self):
        """
        getting the completed command when got incomplete command.
        :return:
        """
        # add_command('a', parser=self.parser)
        expect = ['manager', ]
        line = ['manag', ]
        parser = argument_parser()
        result = ArgumentCmd.get_complete_list(line, parser)
        self.assertListEqual(result, expect)

        expect = ['book']
        line = ['manager', 'bo']
        parser = argument_parser()
        result = ArgumentCmd.get_complete_list(line, parser)
        self.assertListEqual(result, expect)

    def test0110_get_complete_list(self):
        """
        getting next available commands.
        :return:
        """
        expected = ['exit', 'prompt', 'setting', 'manager']
        line = ''.split()
        parser = argument_parser()
        result = ArgumentCmd.get_complete_list(line, parser)
        self.assertListEqual(expected, result)

        expected = ['book']
        line = ['manager', ]
        parser = argument_parser()
        result = ArgumentCmd.get_complete_list(line, parser)
        self.assertListEqual(expected, result)

    def test0110_get_complete_list_all_available_command_options(self):
        """
        getting next available commands.
        :return:
        """
        expected = ['-r', '--raw-data',
                    '-t', '--simple-table',
                    'insert', 'update', 'delete']

        line = 'manager book '.split()
        parser = argument_parser()
        result = ArgumentCmd.get_complete_list(line, parser)
        self.assertListEqual(expected, result)

        expected = ['-r', '--raw-data',
                    '-t', '--simple-table',]

        line = 'manager book -'.split()
        parser = argument_parser()
        result = ArgumentCmd.get_complete_list(line, parser)
        self.assertListEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
