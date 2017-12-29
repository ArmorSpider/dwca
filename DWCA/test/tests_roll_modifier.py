import unittest

from definitions import ROLL_MODIFIERS
from src.modifiers.roll_modifier import RollModifier, add_roll_modifier,\
    OTHER_MODS, RANGE_MOD, get_effective_modifier


class Test(unittest.TestCase):

    def test_unique_key_none_should_set_key_to_other_mods(self):
        roll_modifier = RollModifier(modifier_value=10, unique_key=None)
        expected = OTHER_MODS
        actual = roll_modifier.key

        self.assertEqual(expected, actual)

    def test_generic_modifier_should_be_added_to_other_mods(self):
        roll_modifier = RollModifier(modifier_value=10, unique_key=None)
        event = {}
        expected = {ROLL_MODIFIERS: {OTHER_MODS: [10]}}

        actual = add_roll_modifier(event, roll_modifier)
        self.assertEqual(expected, actual)

    def test_generic_modifier_value_should_use_modifier_value(self):
        roll_modifier = RollModifier(modifier_value=20, unique_key=None)
        event = {}
        expected = {ROLL_MODIFIERS: {OTHER_MODS: [20]}}

        actual = add_roll_modifier(event, roll_modifier)
        self.assertEqual(expected, actual)

    def test_multiple_generic_modifiers_should_append(self):
        roll_modifier_1 = RollModifier(modifier_value=10, unique_key=None)
        roll_modifier_2 = RollModifier(modifier_value=20, unique_key=None)
        event = {}
        expected = {ROLL_MODIFIERS: {OTHER_MODS: [10, 20]}}

        event = add_roll_modifier(event, roll_modifier_1)
        actual = add_roll_modifier(event, roll_modifier_2)
        self.assertEqual(expected, actual)

    def test_specifc_modifier_should_be_added_with_key(self):
        roll_modifier = RollModifier(modifier_value=10, unique_key=RANGE_MOD)
        event = {}
        expected = {ROLL_MODIFIERS: {RANGE_MOD: [10]}}

        actual = add_roll_modifier(event, roll_modifier)
        self.assertEqual(expected, actual)

    def test_multiple_modifiers_with_same_key_should_only_save_latest(self):
        roll_modifier_1 = RollModifier(modifier_value=10, unique_key=RANGE_MOD)
        roll_modifier_2 = RollModifier(modifier_value=20, unique_key=RANGE_MOD)
        event = {}
        expected = {ROLL_MODIFIERS: {RANGE_MOD: [20]}}

        event = add_roll_modifier(event, roll_modifier_1)
        actual = add_roll_modifier(event, roll_modifier_2)
        self.assertEqual(expected, actual)

    def test_adding_the_same_specific_mod_again_should_remove_it(self):
        roll_modifier_1 = RollModifier(modifier_value=10, unique_key=RANGE_MOD)
        roll_modifier_2 = RollModifier(modifier_value=10, unique_key=RANGE_MOD)
        event = {}
        expected = {ROLL_MODIFIERS: {}}

        event = add_roll_modifier(event, roll_modifier_1)
        actual = add_roll_modifier(event, roll_modifier_2)
        self.assertEqual(expected, actual)

    def test_one_generic_one_specific_modifier_should_match_expectations(self):
        roll_modifier_1 = RollModifier(modifier_value=10, unique_key=None)
        roll_modifier_2 = RollModifier(modifier_value=20, unique_key=RANGE_MOD)
        event = {}
        expected = {ROLL_MODIFIERS: {OTHER_MODS: [10], RANGE_MOD: [20]}}

        event = add_roll_modifier(event, roll_modifier_1)
        actual = add_roll_modifier(event, roll_modifier_2)
        self.assertEqual(expected, actual)

    def test_get_effective_modifier_should_support_multiple_positive_modifiers(self):
        event = {ROLL_MODIFIERS: {OTHER_MODS: [10], RANGE_MOD: [20]}}
        expected = 30
        actual = get_effective_modifier(event)
        self.assertEqual(expected, actual)

    def test_get_effective_modifier_should_support_multiple_negative_modifiers(self):
        event = {ROLL_MODIFIERS: {OTHER_MODS: [-10], RANGE_MOD: [-20]}}
        expected = -30
        actual = get_effective_modifier(event)
        self.assertEqual(expected, actual)

    def test_get_effective_modifier_should_support_multiple_mixed_modifiers(self):
        event = {ROLL_MODIFIERS: {OTHER_MODS: [10], RANGE_MOD: [-20]}}
        expected = -10
        actual = get_effective_modifier(event)
        self.assertEqual(expected, actual)

    def test_get_effective_modifier_should_cap_at_negative_60(self):
        event = {ROLL_MODIFIERS: {OTHER_MODS: [-10], RANGE_MOD: [-60]}}
        expected = -60
        actual = get_effective_modifier(event)
        self.assertEqual(expected, actual)

    def test_get_effective_modifier_should_cap_at_positive_60(self):
        event = {ROLL_MODIFIERS: {OTHER_MODS: [10], RANGE_MOD: [60]}}
        expected = 60
        actual = get_effective_modifier(event)
        self.assertEqual(expected, actual)
