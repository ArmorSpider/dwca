import unittest

from src.action.attack import Attack
from src.entities.char_stats import STAT_STR
from src.entities.character import build_character
from src.entities.weapon import Weapon, get_weapon
from src.modifiers.qualities import Proven, MultiplyStrength
from test.test_util import build_mock_weapon, build_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        self.dummy = build_character('dummy')
        self.dummy_weapon = get_weapon('dummy')
        self.proven_5_weapon = Weapon({'name': 'proven_weapon',
                                       'qualities': {Proven.name: 5}})
        self.proven_3_weapon = Weapon({'name': 'proven_weapon',
                                       'qualities': {Proven.name: 3}})

    def test_proven_5_weapon_should_modify_minumum_damage_to_5(self):
        weapon = self.proven_5_weapon
        attack = Attack(attacker=self.dummy, weapon=weapon, target=self.dummy)
        roll_results = [9, 1, 1, 1]
        expected = [9, 5, 5, 5]
        actual = Proven.handle_proven(attack, roll_results)
        self.assertEqual(expected, actual)

    def test_proven_3_weapon_should_modify_minumum_damage_to_3(self):
        weapon = self.proven_3_weapon
        attack = Attack(attacker=self.dummy, weapon=weapon, target=self.dummy)
        roll_results = [9, 1, 1, 1]
        expected = [9, 3, 3, 3]
        actual = Proven.handle_proven(attack, roll_results)
        self.assertEqual(expected, actual)

    def test_non_proven_weapon_should_not_modify_damage(self):
        weapon = self.dummy_weapon
        attack = Attack(attacker=self.dummy, weapon=weapon, target=self.dummy)
        roll_results = [9, 1, 1, 1]
        expected = [9, 1, 1, 1]
        actual = Proven.handle_proven(attack, roll_results)
        self.assertEqual(expected, actual)

    def test_multiply_strength_from_attacker_stats(self):
        attacker = build_mock_entity('MockMan',
                                     characteristics={STAT_STR: 50},
                                     traits={'unnatural_strength': 2})
        weapon = build_mock_weapon('Mock', 'Melee', qualities={
                                   MultiplyStrength.name: 1})
        target = None
        attack = Attack(weapon, attacker, target)
        current = 10

        expected = 15
        actual = MultiplyStrength().modify_damage(attack, current)

        self.assertEqual(expected, actual)

    def test_multiply_strength_from_weapon_stats(self):
        attacker = build_mock_entity('MockMan',
                                     characteristics={STAT_STR: 50},
                                     traits={'unnatural_strength': 2})
        weapon = build_mock_weapon('Mock',
                                   'Melee',
                                   qualities={MultiplyStrength.name: 1},
                                   characteristics={STAT_STR: 60}
                                   )
        target = None
        attack = Attack(weapon, attacker, target)
        current = 10

        expected = 16
        actual = MultiplyStrength().modify_damage(attack, current)

        self.assertEqual(expected, actual)
