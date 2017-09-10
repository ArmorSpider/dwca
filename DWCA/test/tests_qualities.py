import unittest

from src.action.attack import Attack
from src.entities.character import get_char
from src.entities.weapon import Weapon, get_weapon
from src.modifiers.qualities import Proven


class Test(unittest.TestCase):

    def setUp(self):
        self.dummy = get_char('dummy')
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
