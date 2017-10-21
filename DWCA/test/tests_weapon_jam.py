from unittest import TestCase

from src.action.ranged_attack import RangedAttack
from src.dice import queue_rolls
from src.entities import QUALITIES, SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.weapon import Weapon, get_weapon
from src.modifiers.qualities import Reliable, NeverJams
from src.situational.weapon_jam import is_weapon_jammed


class Test(TestCase):

    def setUp(self):
        self.dummy_weapon = get_weapon('dummy_ranged')
        self.jammed_attack_single_shot = RangedAttack(attacker=None,
                                                      weapon=self.dummy_weapon,
                                                      target=None,
                                                      firemode=None)
        self.jammed_attack_single_shot.roll_target = 200
        self.jammed_attack_single_shot.roll_result = 96
        self.reliable_weapon = Weapon({QUALITIES: {Reliable.name: True}})

    def test_single_shot_roll_result_96_should_return_true(self):
        qualities = {}
        attack = self._build_attack(roll_result=96,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = True
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_94_should_return_false(self):
        qualities = {}
        attack = self._build_attack(roll_result=94,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = False
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_semi_auto_roll_result_94_should_return_true(self):
        qualities = {}
        attack = self._build_attack(roll_result=94,
                                    firemode=SEMI_AUTO,
                                    qualities=qualities)
        expected = True
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_full_auto_roll_result_94_should_return_true(self):
        qualities = {}
        attack = self._build_attack(roll_result=94,
                                    firemode=FULL_AUTO,
                                    qualities=qualities)
        expected = True
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_96_and_reliable_roll_1_should_return_false(self):
        queue_rolls([1])
        qualities = {Reliable.name: True}
        attack = self._build_attack(roll_result=96,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = False
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_semi_auto_roll_result_94_and_reliable_roll_1_should_return_false(self):
        queue_rolls([1])
        qualities = {Reliable.name: True}
        attack = self._build_attack(roll_result=94,
                                    firemode=SEMI_AUTO,
                                    qualities=qualities)
        expected = False
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_full_auto_roll_result_94_and_reliable_roll_1_should_return_false(self):
        queue_rolls([1])
        qualities = {Reliable.name: True}
        attack = self._build_attack(roll_result=94,
                                    firemode=SEMI_AUTO,
                                    qualities=qualities)
        expected = False
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_96_and_reliable_10_should_return_true(self):
        queue_rolls([10])
        qualities = {Reliable.name: True}
        attack = self._build_attack(roll_result=96,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = True
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_single_shot_roll_result_96_and_never_jam_should_return_false(self):
        qualities = {NeverJams.name: True}
        attack = self._build_attack(roll_result=96,
                                    firemode=SINGLE_SHOT,
                                    qualities=qualities)
        expected = False
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_semi_auto_roll_result_94_and_never_jam_should_return_false(self):
        qualities = {NeverJams.name: True}
        attack = self._build_attack(roll_result=94,
                                    firemode=SEMI_AUTO,
                                    qualities=qualities)
        expected = False
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def test_full_auto_roll_result_94_and_never_jam_should_return_false(self):
        qualities = {NeverJams.name: True}
        attack = self._build_attack(roll_result=94,
                                    firemode=FULL_AUTO,
                                    qualities=qualities)
        expected = False
        actual = is_weapon_jammed(attack)
        self.assertEqual(expected, actual)

    def _build_attack(self, roll_result, firemode, qualities={}):
        weapon = Weapon({QUALITIES: qualities})
        attack = RangedAttack(attacker=None,
                              weapon=weapon,
                              target=None,
                              firemode=firemode)
        attack.roll_target = 200
        attack.roll_result = roll_result
        return attack
