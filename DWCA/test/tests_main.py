
import unittest

from src.dice import queue_d10_rolls
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.char_stats import STAT_TGH
from src.entities.character import build_character
from src.entities.weapon import get_weapon
from src.modifiers.modifier import register_modifiers


# pylint: skip-file
class Test(unittest.TestCase):

    def setUp(self):
        register_modifiers()

    def test_tearing_and_flesh_render_should_give_2_tearing_dice(self):
        target = build_character('dev_genestealer')
        attacker = build_character('dev_john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker._melee_attack(weapon, target)
        expected = 2
        actual = attack.tearing_dice
        self.assertEqual(expected, actual)

    def test_no_auto_confirm_should_not_trigger_fury_if_confirming_is_impossible(self):
        target = build_character('dev_genestealer')
        attacker = build_character('dev_bohn_jobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker._melee_attack(weapon, target)
        attack.try_action(0)
        queue_d10_rolls([10])
        flat_damage = attack.flat_damage
        expected_damage = 10 + flat_damage

        actual_damage = attack.raw_damage
        self.assertEqual(expected_damage, actual_damage)

    def test_deathwatch_training_should_auto_confirm_against_aliens(self):
        target = build_character('dev_genestealer')
        attacker = build_character('dev_john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker._melee_attack(weapon, target)
        attack.try_action(0)
        queue_d10_rolls([10, 0, 0, 5])  # two tearing dice
        flat_damage = attack.flat_damage
        expected_damage = 10 + 5 + flat_damage
        actual_damage = attack.raw_damage
        self.assertEqual(expected_damage, actual_damage)

    def test_deathwatch_training_should_not_auto_confirm_against_non_aliens(self):
        target = build_character('dev_bohn_jobb')
        attacker = build_character('dev_john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker._melee_attack(weapon, target)
        attack.try_action(0)
        queue_d10_rolls([10])
        flat_damage = attack.flat_damage
        expected_damage = 10 + flat_damage
        actual_damage = attack.raw_damage
        self.assertEqual(expected_damage, actual_damage)

    def test_felling_should_reduce_toughness_multiplier_but_not_below_1(self):
        target = build_character('dev_bohn_jobb')
        attacker = build_character('dev_john_bobb')
        weapon = get_weapon('dev_felling_chainsword')
        attack = attacker._melee_attack(weapon, target)
        attack.try_action(100, 1)

        expected_raw_toughness = 10
        expected_effective_toughness = 5
        actual_effective_toughness = target.get_modded_toughness_bonus(
            attack)
        actual_raw_toughness = target.get_characteristic_bonus(STAT_TGH)

        self.assertEqual(expected_effective_toughness,
                         actual_effective_toughness)
        self.assertEqual(expected_raw_toughness,
                         actual_raw_toughness)

    def test_single_shot(self):
        target = build_character('dev_bohn_jobb')
        attacker = build_character('dev_john_bobb')
        weapon = get_weapon('dev_bolter')
        attack = attacker._ranged_attack(weapon, target, firemode=SINGLE_SHOT)
        attack.try_action(100, 1)

        expected = 1
        actual = attack.num_hits
        self.assertEqual(expected, actual)

    def test_semi_auto(self):
        target = build_character('dev_bohn_jobb')
        attacker = build_character('dev_john_bobb')
        weapon = get_weapon('dev_bolter')
        attack = attacker._ranged_attack(weapon, target, firemode=SEMI_AUTO)
        attack.try_action(100, 1)

        expected = 3
        actual = attack.num_hits
        self.assertEqual(expected, actual)

    def test_full_auto(self):
        target = build_character('dev_bohn_jobb')
        attacker = build_character('dev_john_bobb')
        weapon = get_weapon('dev_bolter')
        attack = attacker._ranged_attack(weapon, target, firemode=FULL_AUTO)
        attack.try_action(100, 1)

        expected = 5
        actual = attack.num_hits
        self.assertEqual(expected, actual)
