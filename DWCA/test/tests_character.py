
import unittest

from src.entities import ARMOR, CHARACTERISTICS, TRAITS
from src.entities.char_stats import STAT_WS, STAT_BS, STAT_STR, STAT_TGH,\
    STAT_AGI, STAT_INT, STAT_PER, STAT_WIL, STAT_FEL
from src.entities.character import Character
from src.hit_location import HITLOC_ALL, HITLOC_BODY, HitLocation


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
                     'unnatural_agility': 4},
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

        self.char_with_stats = Character(character_with_characteristics)
        self.character = Character(character_definition)

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
