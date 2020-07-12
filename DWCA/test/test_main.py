
import unittest

from src.dice import queue_d10_rolls
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.char_stats import STAT_TGH, STAT_STR, STAT_WS
from src.modifiers.modifier import register_modifiers
from test.test_util import build_mock_entity, build_mock_weapon


# pylint: skip-file
class Test(unittest.TestCase):

    def setUp(self):
        register_modifiers()
        self.dev_gs = build_mock_entity('dev_genestealer',
                                        _system='deathwatch',
                                        species='Tyranid',
                                        characteristics={STAT_STR: 60,
                                                         STAT_TGH: 60,
                                                         STAT_WS: 65})
        self.john_bobb = build_mock_entity('dev_john_bobb',
                                           _system='deathwatch',
                                           species='human',
                                           characteristics={STAT_STR: 45,
                                                            STAT_TGH: 51,
                                                            STAT_WS: 45},
                                           talents={'deathwatch_training': True,
                                                    'flesh_render': True},
                                           traits={'unnatural_strength': 2,
                                                   'unnatural_toughness': 2},
                                           armor={'all': 8, 'body': 10})
        self.bohn_jobb = build_mock_entity('dev_bohn_jobb',
                                           _system='deathwatch',
                                           species='human',
                                           characteristics={STAT_STR: 45,
                                                            STAT_TGH: 51,
                                                            STAT_WS: 45},
                                           talents={'touched_by_the_fates': True,
                                                    'flesh_render': True},
                                           traits={'unnatural_strength': 2,
                                                   'unnatural_toughness': 2},
                                           armor={'all': 8, 'body': 10})
        self.chainsword = build_mock_weapon('Dev Chainsword',
                                            'Melee',
                                            _system='deathwatch',
                                            damage_type='R',
                                            dice=1,
                                            flat_damage=3,
                                            penetration=3,
                                            qualities={'balanced': True, 'tearing': True})
        self.bolter = build_mock_weapon('Dev Bolter',
                                        'Basic',
                                        _system='deathwatch',
                                        damage_type='R',
                                        dice=1,
                                        flat_damage=9,
                                        full_auto=5,
                                        semi_auto=3,
                                        single_shot=1,
                                        range=100,
                                        qualities={'tearing': True})
        self.felling_chainsword = build_mock_weapon('Felling Chainsword',
                                                    'Melee',
                                                    _system='deathwatch',
                                                    damage_type='R',
                                                    dice=1,
                                                    flat_damage=3,
                                                    penetration=3,
                                                    qualities={'balanced': True, 'tearing': True, 'felling': 2})

    def test_tearing_and_flesh_render_should_give_2_tearing_dice(self):
        target = self.dev_gs
        attacker = self.john_bobb
        weapon = self.chainsword
        attack = attacker._melee_attack(weapon, target)
        expected = 2
        actual = attack.tearing_dice
        self.assertEqual(expected, actual)

    def test_no_auto_confirm_should_not_trigger_fury_if_confirming_is_impossible(self):
        target = self.dev_gs
        attacker = self.bohn_jobb
        weapon = self.chainsword
        attack = attacker._melee_attack(weapon, target)
        attack.try_action(0)
        queue_d10_rolls([10])
        flat_damage = attack.flat_damage
        expected_damage = 10 + flat_damage

        actual_damage = attack.raw_damage
        self.assertEqual(expected_damage, actual_damage)

    def test_deathwatch_training_should_auto_confirm_against_aliens(self):
        target = self.dev_gs
        attacker = self.john_bobb
        weapon = self.chainsword
        attack = attacker._melee_attack(weapon, target)
        attack.try_action(0)
        queue_d10_rolls([10, 0, 0, 5])  # two tearing dice
        flat_damage = attack.flat_damage
        expected_damage = 10 + 5 + flat_damage
        actual_damage = attack.raw_damage
        self.assertEqual(expected_damage, actual_damage)

    def test_deathwatch_training_should_not_auto_confirm_against_non_aliens(self):
        target = self.bohn_jobb
        attacker = self.john_bobb
        weapon = self.chainsword
        attack = attacker._melee_attack(weapon, target)
        attack.try_action(0)
        queue_d10_rolls([10])
        flat_damage = attack.flat_damage
        expected_damage = 10 + flat_damage
        actual_damage = attack.raw_damage
        self.assertEqual(expected_damage, actual_damage)

    def test_felling_should_reduce_toughness_multiplier_but_not_below_1(self):
        target = self.bohn_jobb
        attacker = self.john_bobb
        weapon = self.felling_chainsword
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
        target = self.bohn_jobb
        attacker = self.john_bobb
        weapon = self.bolter
        attack = attacker._ranged_attack(weapon, target, firemode=SINGLE_SHOT)
        attack.try_action(100, 1)

        expected = 1
        actual = attack.num_hits
        self.assertEqual(expected, actual)

    def test_semi_auto(self):
        target = self.bohn_jobb
        attacker = self.john_bobb
        weapon = self.bolter
        attack = attacker._ranged_attack(weapon, target, firemode=SEMI_AUTO)
        attack.try_action(100, 1)

        expected = 3
        actual = attack.num_hits
        self.assertEqual(expected, actual)

    def test_full_auto(self):
        target = self.bohn_jobb
        attacker = self.john_bobb
        weapon = self.bolter
        attack = attacker._ranged_attack(weapon, target, firemode=FULL_AUTO)
        attack.try_action(100, 1)

        expected = 5
        actual = attack.num_hits
        self.assertEqual(expected, actual)
