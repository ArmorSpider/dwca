from random import choice
import unittest

from mock import patch

from src.cli.commands import process_command
from src.cli.new_module import new_module
from src.entities.libraries import MasterLibrary
from src.errors import OutOfRangeError
from src.util.dict_util import pretty_print
from src.util.rand_util import _random_int


def return_random(list_):
    thing = choice(list_)
    print 'Chose "%s"' % thing
    return thing


def return_number(prompt):
    return _random_int(1, 100)


class Test(unittest.TestCase):

    def setUp(self):
        MasterLibrary.load_all_packages()
        self.random_commands = ['info',
                                'bonus',
                                'malus',
                                'range',
                                'equip',
                                'attacker',
                                'target',
                                'overload',
                                'cover',
                                'charge',
                                'aim',
                                'auto']

    @patch('src.util.user_input.user_choose_from_list', side_effect=return_random)
    @patch('src.util.user_input.user_input_int', side_effect=return_number)
    @patch('src.cli.commands.user_input_int', side_effect=return_number)
    def test_run_random_attacks(self, _1, _2, _3):
        for _ in range(100):
            self._run_random_attack()

    def _run_random_attack(self):
        event = new_module({})
        pretty_print(event)
        event = self._run_random_command(event)
        process_command('run', event)

    def _run_random_command(self, event):
        command = choice(self.random_commands)
        print 'RAN "%s"' % command
        try:
            event = process_command(command, event)
        except OutOfRangeError:
            pass
        return event
