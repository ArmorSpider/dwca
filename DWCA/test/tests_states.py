import unittest

from definitions import ROLL_TARGET, EFFECTIVE_TOUGHNESS, EFFECTIVE_DAMAGE,\
    EFFECTIVE_ARMOR
from src.entities import ARMOR, CHARACTERISTICS, FLAT_DAMAGE, PENETRATION,\
    QUALITIES
from src.entities.char_stats import STAT_TGH
from src.modifiers.states import IgnoreArmor, IgnoreToughness, TrueDamage
from test.simulate_attack import simulate_attack


class Test(unittest.TestCase):

    def setUp(self):
        self.spaceman_def = {'_system': 'deathwatch',
                             ARMOR: {'all': 10},
                             CHARACTERISTICS: {STAT_TGH: 50}}

    def test_baseline_for_mitigation_bypass(self):
        event = {ROLL_TARGET: 50}
        die_rolls = [20, 5]
        expected_damage = [10]
        expected_armor = [10]
        expected_toughness = [5]

        weapon_def = {FLAT_DAMAGE: 20,
                      PENETRATION: 0}

        metadata = simulate_attack(event,
                                   die_rolls,
                                   weapon_def=weapon_def,
                                   target_def=self.spaceman_def)

        actual_damage = metadata[EFFECTIVE_DAMAGE]
        actual_armor = metadata[EFFECTIVE_ARMOR]
        actual_toughness = metadata[EFFECTIVE_TOUGHNESS]

        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_armor, actual_armor)
        self.assertEqual(expected_toughness, actual_toughness)

    def test_ignore_armor_should_set_effective_armor_to_zero(self):
        event = {ROLL_TARGET: 50}
        die_rolls = [20, 5]
        expected_damage = [20]
        expected_armor = [0]
        expected_toughness = [5]

        weapon_def = {FLAT_DAMAGE: 20,
                      PENETRATION: 0,
                      QUALITIES: {IgnoreArmor.name: True}}

        metadata = simulate_attack(event,
                                   die_rolls,
                                   weapon_def=weapon_def,
                                   target_def=self.spaceman_def)

        actual_damage = metadata[EFFECTIVE_DAMAGE]
        actual_armor = metadata[EFFECTIVE_ARMOR]
        actual_toughness = metadata[EFFECTIVE_TOUGHNESS]

        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_armor, actual_armor)
        self.assertEqual(expected_toughness, actual_toughness)

    def test_ignore_toughness_should_set_effective_toughness_to_zero(self):
        event = {ROLL_TARGET: 50}
        die_rolls = [20, 5]
        expected_damage = [15]
        expected_armor = [10]
        expected_toughness = [0]

        weapon_def = {FLAT_DAMAGE: 20,
                      PENETRATION: 0,
                      QUALITIES: {IgnoreToughness.name: True}}

        metadata = simulate_attack(event,
                                   die_rolls,
                                   weapon_def=weapon_def,
                                   target_def=self.spaceman_def)

        actual_damage = metadata[EFFECTIVE_DAMAGE]
        actual_armor = metadata[EFFECTIVE_ARMOR]
        actual_toughness = metadata[EFFECTIVE_TOUGHNESS]

        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_armor, actual_armor)
        self.assertEqual(expected_toughness, actual_toughness)

    def test_true_damage_should_set_armor_and_tougness_to_zero(self):
        event = {ROLL_TARGET: 50}
        die_rolls = [20, 5]
        expected_damage = [25]
        expected_armor = [0]
        expected_toughness = [0]

        weapon_def = {FLAT_DAMAGE: 20,
                      PENETRATION: 0,
                      QUALITIES: {TrueDamage.name: True}}

        metadata = simulate_attack(event,
                                   die_rolls,
                                   weapon_def=weapon_def,
                                   target_def=self.spaceman_def)

        actual_damage = metadata[EFFECTIVE_DAMAGE]
        actual_armor = metadata[EFFECTIVE_ARMOR]
        actual_toughness = metadata[EFFECTIVE_TOUGHNESS]

        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_armor, actual_armor)
        self.assertEqual(expected_toughness, actual_toughness)
