import unittest
from src.cli.commands import CommandRun


class Test(unittest.TestCase):

    def test_non_matching_strings_should_return_false(self):
        command_strings = ['', 'auto', 'aiwhjdawpid', '721']
        run_command = CommandRun()
        for command_string in command_strings:
            self.assertFalse(run_command.is_this_command(command_string))

    def test_fully_matching_string_should_return_true(self):
        run_command = CommandRun()
        command_strings = [run_command.keyword]
        for command_string in command_strings:
            self.assertTrue(run_command.is_this_command(command_string))

    def test_strings_with_command_as_part_should_not_match(self):
        command_strings = ['runninger', 'run for your life', 'runes']
        run_command = CommandRun()
        for command_string in command_strings:
            self.assertFalse(run_command.is_this_command(command_string))

    def test_strings_wihtin_normalization_should_match(self):
        command_strings = ['RUN', 'Run', '     run',
                           '   run        ', 'ruN     ']
        run_command = CommandRun()
        for command_string in command_strings:
            self.assertTrue(run_command.is_this_command(command_string))