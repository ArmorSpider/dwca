
import unittest

from definitions import PROTECTION_MAX, OVERLOAD_MAX
from src.action.attack import Attack
from src.entities import ARMOR, CHARACTERISTICS, TRAITS, TALENTS, HALF_MOVE,\
    FULL_MOVE, CHARGE_MOVE, RUN_MOVE
from src.entities.char_stats import STAT_WS, STAT_BS, STAT_STR, STAT_TGH,\
    STAT_AGI, STAT_INT, STAT_PER, STAT_WIL, STAT_FEL
from src.entities.character import Character
from src.hit_location import HITLOC_ALL, HITLOC_BODY, HitLocation, BODY, HEAD
from src.modifiers.modifier import register_modifiers
from src.situational.force_field import ForceField
from test.test_util import build_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        character_definition = {
            ARMOR: {HITLOC_ALL: 8,
                    HITLOC_BODY: 10
                    }

        }
        character_with_characteristics = {
            TRAITS: {'unnatural_strength': 2,
                     'unnatural_toughness': 3,
                     'unnatural_agility': 4,
                     'size': 20},
            TALENTS: {'good_listener': True},
            STAT_TGH: {'all': 2, 'head': 1},
            CHARACTERISTICS: {STAT_WS: 10,
                              STAT_BS: 20,
                              STAT_STR: 29,
                              STAT_TGH: 35,
                              STAT_AGI: 30,
                              STAT_INT: 40,
                              STAT_PER: 50,
                              STAT_WIL: 60,
                              STAT_FEL: 70,
                              }

        }
        self.force_field_char_def = {'name': 'Mr. Force Field', 'force_field': {
            PROTECTION_MAX: 65, OVERLOAD_MAX: 10}}
        self.char_with_force_field = Character(self.force_field_char_def)

        self.char_with_stats = Character(character_with_characteristics)
        self.character = Character(character_definition)
        self.char_with_bonuses = build_mock_entity('BonusMan',
                                                   _system='deathwatch',
                                                   characteristics={STAT_STR: 50,
                                                                    STAT_STR + '_bonus': 20,
                                                                    STAT_TGH: 30,
                                                                    STAT_TGH + '_bonus': 50},
                                                   traits={'unnatural_strength': 2,
                                                           'unnatural_toughness': 2})
        register_modifiers()

    def test_get_armor_for_hitloc_should_return_all_value_if_hitloc_not_available(self):
        expected = 8
        actual = self.character.get_armor('head')

        self.assertEqual(expected, actual)

    def test_get_armor_for_hitloc_should_support_both_string_and_enum(self):
        expected = 8
        actual = self.character.get_armor(HitLocation.HEAD)

        self.assertEqual(expected, actual)

    def test_get_armor_for_hitloc_should_return_specific_value_if_available(self):
        expected = 10
        actual = self.character.get_armor(HITLOC_BODY)

        self.assertEqual(expected, actual)

    def test_get_armor_for_hitloc_should_return_0_if_hitloc_not_available_and_no_all_is_defined(self):
        character_definition = {
            ARMOR: {}
        }
        character = Character(character_definition)
        expected = 0
        actual = character.get_armor(HITLOC_BODY)

        self.assertEqual(expected, actual)

    def test_get_characteristic_for_undefined_characteristic_should_return_0(self):
        expected = 0
        characteristic = 'coolness'

        actual = self.char_with_stats.get_characteristic(characteristic)
        self.assertEqual(expected, actual)

    def test_get_characteristic_should_return_raw_characteristic(self):
        expected_values = [10, 29, 35, 70]
        characteristics = [STAT_WS, STAT_STR, STAT_TGH, STAT_FEL]

        for expected, characteristic in zip(expected_values, characteristics):
            actual = self.char_with_stats.get_characteristic(characteristic)
            self.assertEqual(expected, actual)

    def test_get_characteristic_bonus_should_get_tens_from_characteristic(self):
        expected_values = [4, 5, 6, 7]
        characteristics = [STAT_INT, STAT_PER, STAT_WIL, STAT_FEL]

        for expected, characteristic in zip(expected_values, characteristics):
            actual = self.char_with_stats.get_characteristic_bonus(
                characteristic)
            self.assertEqual(expected, actual)

    def test_get_characteristic_bonus_should_include_unnatural_traits(self):
        expected = 12
        actual = self.char_with_stats.get_characteristic_bonus(STAT_AGI)

        self.assertEqual(expected, actual)

    def test_unnatural_traits_should_only_multiply_tens(self):
        expected = 4
        actual = self.char_with_stats.get_characteristic_bonus(STAT_STR)

        self.assertEqual(expected, actual)

    def test_get_force_field_should_return_force_field(self):
        expected = ForceField({PROTECTION_MAX: 65, OVERLOAD_MAX: 10})
        actual = self.char_with_force_field.force_field

        self.assertEqual(expected, actual)

    def test_modifers_should_include_traits_and_talents(self):
        expected = {'unnatural_strength': 2,
                    'unnatural_toughness': 3,
                    'unnatural_agility': 4,
                    'good_listener': True,
                    'size': 20}
        actual = self.char_with_stats.modifiers
        self.assertEqual(expected, actual)

    def test_size_bonus_should_return_size_trait_value(self):
        expected = 20
        actual = self.char_with_stats.size_bonus
        self.assertEqual(expected, actual)

    def test_size_bonus_with_no_size_specified_should_return_zero(self):
        expected = 0
        actual = self.char_with_force_field.size_bonus
        self.assertEqual(expected, actual)

    def test_get_modded_toughness_bonus_should_include_locational_toughness(self):
        expected = 10
        attack = Attack(None, None, None)
        actual = self.char_with_stats.get_modded_toughness_bonus(
            attack, HEAD)
        self.assertEqual(expected, actual)

    def test_locational_toughness_should_be_applied_after_multipliers(self):
        expected = 4
        attack = Attack(None, None, None)
        attack.ad_hoc_modifiers = {'felling': 25}
        actual = self.char_with_stats.get_modded_toughness_bonus(
            attack, HEAD)
        self.assertEqual(expected, actual)

    def test_locational_toughness_should_support_all_key(self):
        expected = 11
        attack = Attack(None, None, None)
        actual = self.char_with_stats.get_modded_toughness_bonus(
            attack, BODY)
        self.assertEqual(expected, actual)

    def test_black_carapace_should_set_size_bonus_to_zero(self):
        mockman = build_mock_entity('Mockman',
                                    traits={'size': 10, 'black_carapace': True})
        expected = 0
        actual = mockman.size_bonus
        self.assertEqual(expected, actual)

    def test_getattr_should_do_lookup_in_modifiers(self):
        self.assertEqual(2, self.char_with_stats.unnatural_strength)
        self.assertEqual(3, self.char_with_stats.unnatural_toughness)
        self.assertEqual(4, self.char_with_stats.unnatural_agility)
        self.assertEqual(True, self.char_with_stats.good_listener)

    def test_getting_attribute_that_does_not_exist_in_modifers_should_raise_attributeerror(self):
        with self.assertRaises(AttributeError):
            self.char_with_stats.THIS_IS_NOT_A_REAL_ATTRIBUTE

    def test_getting_attribute_that_does_not_exist_in_modifiers_but_is_a_known_modifier_should_return_none(self):
        expected = None
        actual = self.char_with_stats.toxic
        self.assertEqual(expected, actual)

    def test_flat_stat_bonuses_should_not_be_included_in_unnatural_characteristics(self):
        expected = 12
        actual = self.char_with_bonuses.get_characteristic_bonus(STAT_STR)

        self.assertEqual(expected, actual)

    def test_flat_stat_bonuses_should_not_be_included_characteristic_value(self):
        expected = 70
        actual = self.char_with_bonuses.get_characteristic(STAT_STR)

        self.assertEqual(expected, actual)

    def test_flat_stat_bonus_should_work_for_toughness(self):
        expected = 11
        attack = Attack(None, None, None)
        actual = self.char_with_bonuses.get_modded_toughness_bonus(attack)

        self.assertEqual(expected, actual)
