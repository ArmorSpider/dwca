
import unittest

from main import boosh
from src.dice import queue_rolls
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.char_stats import STAT_TGH
from src.entities.character import get_char
from src.entities.weapon import get_weapon
from src.modifiers.modifier import register_modifiers


# pylint: skip-file
class Test(unittest.TestCase):

    def setUp(self):
        register_modifiers()

    def test_genestealer(self):
        attacker = get_char('dev_genestealer')
        target = get_char('dev_john_bobb')
        weapon = get_weapon('rending_claws')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(96, 1)
        expected_dice = 1
        expected_pen = 10
        expected_damage = 14
        expected_dos = 9

        actual_dice = attack._get_num_dice()
        actual_pen = attack._get_penetration()
        actual_damage = attack._get_flat_damage()
        actual_dos = attack.get_degrees_of_success()

        self.assertEqual(expected_dice, actual_dice)
        self.assertEqual(expected_pen, actual_pen)
        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_dos, actual_dos)

    def test_tearing_and_flesh_render_should_give_2_tearing_dice(self):
        target = get_char('dev_genestealer')
        attacker = get_char('dev_john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        expected = 2
        actual = attack._get_tearing_dice()
        self.assertEqual(expected, actual)

    def test_no_auto_confirm_should_not_trigger_fury_if_confirming_is_impossible(self):
        target = get_char('dev_genestealer')
        attacker = get_char('dev_bohn_jobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(0)
        queue_rolls([10])
        flat_damage = attack._get_flat_damage()
        expected_damage = 10 + flat_damage

        actual_damage = attack._roll_damage()
        self.assertEqual(expected_damage, actual_damage)

    def test_deathwatch_training_should_auto_confirm_against_aliens(self):
        target = get_char('dev_genestealer')
        attacker = get_char('dev_john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(0)
        queue_rolls([10, 0, 0, 5])  # two tearing dice
        flat_damage = attack._get_flat_damage()
        expected_damage = 10 + 5 + flat_damage
        actual_damage = attack._roll_damage()
        self.assertEqual(expected_damage, actual_damage)

    def test_deathwatch_training_should_not_auto_confirm_against_non_aliens(self):
        target = get_char('dev_bohn_jobb')
        attacker = get_char('dev_john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(0)
        queue_rolls([10])
        flat_damage = attack._get_flat_damage()
        expected_damage = 10 + flat_damage
        actual_damage = attack._roll_damage()
        self.assertEqual(expected_damage, actual_damage)

    def test_felling_should_reduce_toughness_multiplier_but_not_below_1(self):
        target = get_char('dev_bohn_jobb')
        attacker = get_char('dev_john_bobb')
        weapon = get_weapon('dev_felling_chainsword')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(100, 1)

        expected_raw_toughness = 10
        expected_effective_toughness = 5
        actual_effective_toughness = target._get_effective_toughness_bonus(
            attack)
        actual_raw_toughness = target.get_characteristic_bonus(STAT_TGH)

        self.assertEqual(expected_effective_toughness,
                         actual_effective_toughness)
        self.assertEqual(expected_raw_toughness,
                         actual_raw_toughness)

    def test_single_shot(self):
        target = get_char('dev_bohn_jobb')
        attacker = get_char('dev_john_bobb')
        weapon = get_weapon('dev_bolter')
        attack = attacker.ranged_attack(weapon, target, firemode=SINGLE_SHOT)
        attack.try_action(100, 1)

        expected = 1
        actual = attack._get_num_hits()
        self.assertEqual(expected, actual)

    def test_semi_auto(self):
        target = get_char('dev_bohn_jobb')
        attacker = get_char('dev_john_bobb')
        weapon = get_weapon('dev_bolter')
        attack = attacker.ranged_attack(weapon, target, firemode=SEMI_AUTO)
        attack.try_action(100, 1)

        expected = 3
        actual = attack._get_num_hits()
        self.assertEqual(expected, actual)

    def test_full_auto(self):
        target = get_char('dev_bohn_jobb')
        attacker = get_char('dev_john_bobb')
        weapon = get_weapon('dev_bolter')
        attack = attacker.ranged_attack(weapon, target, firemode=FULL_AUTO)
        attack.try_action(100, 1)

        expected = 5
        actual = attack._get_num_hits()
        self.assertEqual(expected, actual)
