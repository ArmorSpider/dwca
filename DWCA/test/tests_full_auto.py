from random import choice
import unittest

from mock import patch

from src.cli.commands import process_command
from src.entities.libraries import MasterLibrary
from src.errors import OutOfRangeError
from src.modules.new_module import handler_new
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
        MasterLibrary.reload_libraries()
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
                                'auto',
                                'move',
                                'defend']

    @patch('src.util.user_input.user_choose_from_list', side_effect=return_random)
    @patch('src.util.user_input.user_input_int', side_effect=return_number)
    @patch('src.cli.commands.user_input_int', side_effect=return_number)
    def DISABLED_test_run_random_attacks(self, _1, _2, _3):
        for _ in range(100):
            self._run_random_attack()

    def _run_random_attack(self):
        event = handler_new({})
        pretty_print(event)
        event = self._run_random_command(event)
        process_command('', event)

    def _run_random_command(self, event):
        command = choice(self.random_commands)
        print 'Ran command "%s"' % command
        try:
            event = process_command(command, event)
        except OutOfRangeError:
            pass
        return event
