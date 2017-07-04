import unittest

from hypothesis import strategies as st
from hypothesis.core import given

from src.entities import QUALITIES, TALENTS, TRAITS
from src.entities.attack import Attack
from src.entities.entity import Entity, Character
from src.entities.weapon import Weapon
from src.goal_roll.goal_roll import GoalRoll


class Test(unittest.TestCase):

    def setUp(self):
        self.entity = Character()
        self.weapon = Weapon()
        chainsword_definition = {
            "name": 'Astartes Chainsword',
            "flat_damage": 3,
            "penetration": 3,
            "dice": 1,
            QUALITIES: {
                    "balanced": True,
                    "tearing": True
            }
        }
        space_marine_definition = {
            'name': 'Space Marine',
            TALENTS: {
                    "crushing_blow": True
            },
            TRAITS: {
                "machine": 5,
            }

        }

        self.chainsword = Weapon(definition=chainsword_definition)
        self.space_marine = Character(definition=space_marine_definition)

    def test_attacking_should_return_an_attack(self):
        entity = self.entity
        weapon = self.weapon
        attack = entity.attack(weapon)

        self.assertIsInstance(attack, Attack)

    def test_attack_should_contain_weapon(self):
        entity = self.entity
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = weapon
        actual = attack.get_weapon()

        self.assertEqual(expected, actual)

    def test_attack_should_contain_attacker(self):
        entity = self.entity
        weapon = self.weapon
        attack = entity.attack(weapon=weapon)

        expected = entity
        actual = attack.get_attacker()

        self.assertEqual(expected, actual)

    def test_get_qualities_should_return_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = {'balanced': True, 'tearing': True}
        actual = attack.get_weapon_qualities()

        self.assertEqual(expected, actual)

    def test_get_attacker_traits_should_return_attacker_traits(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = {'machine': 5}
        actual = attack.get_attacker_traits()

        self.assertEqual(expected, actual)

    def test_get_attacker_talents_should_return_attacker_talents(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = {'crushing_blow': True}
        actual = attack.get_attacker_talents()

        self.assertEqual(expected, actual)

    @given(result=st.integers(min_value=1, max_value=100), target=st.integers(min_value=1, max_value=300))
    def test_get_degrees_of_success_should_work(self, result, target):
        goal_roll = GoalRoll(result, target)
        dos = goal_roll.get_degrees_of_success()
        self.assert_dos_calculation(goal_roll, dos)

    def assert_dos_calculation(self, goal_roll, dos):
        _roll_dice = goal_roll.roll_result
        target = goal_roll.target
        diff = target - _roll_dice
        tens = int(diff / 10)
        if tens < 0:
            tens = 0
        # print 'Roll: {}, Target: {}, Diff:{} , DoS: {}'.format(roll_result, target,
        # diff, dos)
        self.assertTrue(dos <= tens)

    def assert_lists_equal(self, expected, actual):
        self.assertEqual(sorted(expected), sorted(actual))
