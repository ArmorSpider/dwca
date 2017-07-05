import unittest

from hypothesis import strategies as st
from hypothesis.core import given

from src.entities import QUALITIES, TALENTS, TRAITS, DICE, DAMAGE, PENETRATION,\
    NAME, ARMOR
from src.action.attack import Attack, Action
from src.entities.entity import Character
from src.entities.weapon import Weapon
from src.hit_location import HitLocation, get_hit_location, HITLOC_ALL,\
    HITLOC_BODY, RIGHT_ARM, BODY, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_LEG
from src.hitloc_series import get_hit_locations


class Test(unittest.TestCase):

    def setUp(self):
        self.entity = Character()
        self.weapon = Weapon()
        chainsword_definition = {
            NAME: 'Astartes Chainsword',
            DAMAGE: 5,
            PENETRATION: 3,
            DICE: 1,
            QUALITIES: {
                'balanced': True,
                'tearing': True
            }
        }
        space_marine_definition = {
            NAME: 'Space Marine',
            TALENTS: {
                'crushing_blow': True
            },
            TRAITS: {
                'machine': 5,
            },
            ARMOR: {HITLOC_ALL: 8,
                    HITLOC_BODY: 10
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

    def test_attack_should_contain_target_if_specified(self):
        entity = self.entity
        weapon = self.weapon
        attack = entity.attack(weapon=weapon, target=entity)

        expected = entity
        actual = attack.get_target()

        self.assertEqual(expected, actual)

    def test_get_qualities_should_return_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = {'balanced': True, 'tearing': True}
        actual = attack._get_weapon_qualities()

        self.assertEqual(expected, actual)

    def test_get_attacker_traits_should_return_attacker_traits(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = {'machine': 5}
        actual = attack._get_attacker_traits()

        self.assertEqual(expected, actual)

    def test_get_attacker_talents_should_return_attacker_talents(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = {'crushing_blow': True}
        actual = attack._get_attacker_talents()

        self.assertEqual(expected, actual)

    def test_get_offensive_modifiers_should_return_attacker_traits_talents_and_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = {'crushing_blow': True,
                    'machine': 5,
                    'balanced': True,
                    'tearing': True}
        actual = attack.get_offensive_modifiers()

        self.assertEqual(expected, actual)

    def test_get_defensive_modifiers_should_return_target_traits_and_talents(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon, target=entity)

        expected = {'crushing_blow': True,
                    'machine': 5}
        actual = attack.get_defensive_modifiers()

        self.assertEqual(expected, actual)

    def test_calculate_num_damage_dice_should_use_weapons_num_dice(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = 1
        actual = attack.calculate_num_dice()

        self.assertEqual(expected, actual)

    def test_calculate_penetration_should_use_weapons_penetration(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = 3
        actual = attack.calculate_penetration()

        self.assertEqual(expected, actual)

    def test_calculate_flat_damage_should_use_weapons_damage(self):
        entity = self.space_marine
        weapon = self.chainsword
        attack = entity.attack(weapon)

        expected = 5
        actual = attack.calculate_flat_damage()

        self.assertEqual(expected, actual)

    def test_get_hit_location_should_work(self):
        input_rolls = [10, 20, 30, 70, 85, 100]
        expected_locations = [HitLocation.HEAD,
                              HitLocation.RIGHT_ARM,
                              HitLocation.LEFT_ARM,
                              HitLocation.BODY,
                              HitLocation.RIGHT_LEG,
                              HitLocation.LEFT_LEG]

        for input_roll, expected_location in zip(input_rolls, expected_locations):
            actual = get_hit_location(input_roll)
            self.assertEqual(expected_location, actual)

    def test_non_matching_hit_location_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            get_hit_location(125)

    def test_get_hit_locations_for_right_arm_should_match_expectations(self):
        expected = [RIGHT_ARM, RIGHT_ARM, BODY, HEAD,
                    BODY,  RIGHT_ARM, RIGHT_ARM, RIGHT_ARM]
        actual = get_hit_locations(HitLocation.RIGHT_ARM, len(expected))
        self.assertEqual(expected, actual)

    def test_get_hit_locations_for_left_arm_should_match_expectations(self):
        expected = [LEFT_ARM, LEFT_ARM, BODY, HEAD,
                    BODY,  LEFT_ARM, LEFT_ARM, LEFT_ARM]
        actual = get_hit_locations(HitLocation.LEFT_ARM, len(expected))
        self.assertEqual(expected, actual)

    def test_get_hit_locations_for_left_leg_should_match_expectations(self):
        expected = [LEFT_LEG, LEFT_LEG, BODY, LEFT_ARM,
                    HEAD, BODY, BODY, BODY]
        actual = get_hit_locations(HitLocation.LEFT_LEG, len(expected))
        self.assertEqual(expected, actual)

    def test_get_hit_locations_for_right_leg_should_match_expectations(self):
        expected = [RIGHT_LEG, RIGHT_LEG, BODY, RIGHT_ARM,
                    HEAD, BODY, BODY, BODY]
        actual = get_hit_locations(HitLocation.RIGHT_LEG, len(expected))
        self.assertEqual(expected, actual)

    @given(result=st.integers(min_value=1, max_value=100), roll_target=st.integers(min_value=1, max_value=300))
    def test_get_degrees_of_success_should_work(self, result, roll_target):
        action = Action()
        action.try_action(roll_target, result)
        dos = action.get_degrees_of_success()
        self.assert_dos_calculation(action, dos)

    def test_get_reverse_should_reverse_roll_result(self):
        input_values = [21, 100, 20, 1]
        expected = [12, 001, 02, 10]

        for input_value, expected_value in zip(input_values, expected):
            action = Action()
            action.try_action(100, roll_result=input_value)
            actual = action.get_reverse()
            self.assertEqual(expected_value, actual)

    def assert_dos_calculation(self, action, dos):
        roll_result = action.roll_result
        roll_target = action.roll_target
        diff = roll_target - roll_result
        tens = int(diff / 10)
        if tens < 0:
            tens = 0
        # print 'Roll: {}, Target: {}, Diff:{} , DoS: {}'.format(roll_result, roll_target,
        # diff, dos)
        self.assertTrue(dos <= tens)

    def assert_lists_equal(self, expected, actual):
        self.assertEqual(sorted(expected), sorted(actual))
