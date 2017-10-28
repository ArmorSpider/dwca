import unittest

from src.action.ranged_attack import RangedAttack
from src.cli.message_queue import log_messages
from src.dice import queue_rolls
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO, QUALITIES, NAME
from src.entities.weapon import Weapon
from src.modifiers.qualities import Reliable, NeverJams, OverHeats


class Test(unittest.TestCase):

    def tearDown(self):
        log_messages()

    def test_single_shot_roll_result_96_should_return_false(self):
        attack = self._build_attack(96, SINGLE_SHOT)
        expected = False
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_96_reliable_1_should_return_false(self):
        qualities = {Reliable.name: True}
        queue_rolls([1])
        attack = self._build_attack(roll_result=96,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = False
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_96_never_jams_should_return_false(self):
        qualities = {NeverJams.name: True}
        queue_rolls([1])
        attack = self._build_attack(roll_result=96,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = False
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_91_overheats_should_return_false(self):
        qualities = {OverHeats.name: True}
        queue_rolls([1])
        attack = self._build_attack(roll_result=91,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = False
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_95_should_return_true(self):
        attack = self._build_attack(95, SINGLE_SHOT)
        expected = True
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_semi_auto_roll_result_94_should_return_false(self):
        attack = self._build_attack(94, SEMI_AUTO)
        expected = False
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_semi_auto_roll_result_93_should_return_true(self):
        attack = self._build_attack(93, SEMI_AUTO)
        expected = True
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_full_auto_roll_result_94_should_return_false(self):
        attack = self._build_attack(94, FULL_AUTO)
        expected = False
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def test_full_auto_roll_result_93_should_return_true(self):
        attack = self._build_attack(93, FULL_AUTO)
        expected = True
        actual = attack.is_successfull()
        self.assertEqual(expected, actual)

    def _build_attack(self, roll_result, firemode, qualities={}):
        weapon = Weapon({QUALITIES: qualities,
                         NAME: 'DevWeapon'})
        attack = RangedAttack(attacker=None,
                              weapon=weapon,
                              target=None,
                              firemode=firemode)
        attack.roll_target = 200
        attack.roll_result = roll_result
        return attack
