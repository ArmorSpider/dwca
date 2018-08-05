import unittest

from definitions import ATTACKER, WEAPON, TARGET, ROLL_TARGET, EFFECTIVE_DAMAGE,\
    EFFECTIVE_ARMOR, CLASS
from src.entities import QUALITIES, FLAT_DAMAGE, PENETRATION, DICE, ARMOR,\
    TRAITS, CHARACTERISTICS
from src.entities.char_stats import STAT_TGH
from src.modifiers.qualities import Sanctified, WarpWeapon, SanctifiedArmor
from test.simulate_attack import simulate_attack
from test.test_util import add_mock_entity, add_mock_weapon


class Test(unittest.TestCase):

    def setUp(self):
        self.attacker_name = add_mock_entity('Dummy Attacker',
                                             _system='deathwatch')
        self.warp_weapon_name = add_mock_weapon('Warpy Weapon',
                                                'Melee',
                                                _system='deathwatch',
                                                qualities={
                                                    WarpWeapon.name: True},
                                                flat_damage=5,
                                                penetration=0)
        self.armor_man_name = add_mock_entity('ARMORMAN',
                                              _system='deathwatch',
                                              armor={'all': 7000})
        self.sanc_offensive_name = add_mock_entity('SancOffensive',
                                                   _system='deathwatch',
                                                   armor={'all': 5},
                                                   traits={
                                                       Sanctified.name: True},
                                                   characteristics={STAT_TGH: 50})
        self.sanc_armor_name = add_mock_entity('SancArmor',
                                               _system='deathwatch',
                                               armor={'all': 5},
                                               traits={
                                                   SanctifiedArmor.name: True},
                                               characteristics={STAT_TGH: 50})

        self.weapon_def = {CLASS: 'Melee',
                           '_system': 'deathwatch',
                           QUALITIES: {WarpWeapon.name: True},
                           FLAT_DAMAGE: 5,
                           DICE: 1,
                           PENETRATION: 0}
        self.target_armor_def = {'_system': 'deathwatch',
                                 ARMOR: {'all': 7000}}
        self.target_sanctified_def = {'_system': 'deathwatch',
                                      ARMOR: {'all': 5},
                                      TRAITS: {Sanctified.name: True},
                                      CHARACTERISTICS: {STAT_TGH: 50}}
        self.target_sanctified_armor_def = {'_system': 'deathwatch',
                                            ARMOR: {'all': 5},
                                            TRAITS: {SanctifiedArmor.name: True},
                                            CHARACTERISTICS: {STAT_TGH: 50}}

    def test_warp_weapon_should_ignore_mundane_armor(self):
        event = {ROLL_TARGET: 50}
        die_rolls = [20, 9]
        expected_damage = [14]
        expected_armor = [0]

        metadata = simulate_attack(event,
                                   die_rolls,
                                   weapon_def=self.weapon_def,
                                   target_def=self.target_armor_def)

        actual_damage = metadata[EFFECTIVE_DAMAGE]
        actual_armor = metadata[EFFECTIVE_ARMOR]

        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_armor, actual_armor)

    def test_sanctified_should_not_protect_against_warp_weapon(self):
        event = {ROLL_TARGET: 50}
        die_rolls = [20, 9]
        expected_damage = [9]
        expected_armor = [0]

        metadata = simulate_attack(event,
                                   die_rolls,
                                   weapon_def=self.weapon_def,
                                   target_def=self.target_sanctified_def)

        actual_damage = metadata[EFFECTIVE_DAMAGE]
        actual_armor = metadata[EFFECTIVE_ARMOR]

        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_armor, actual_armor)

    def test_sanctified_armor_should_protect_against_warp_weapon(self):
        event = {ROLL_TARGET: 50}
        die_rolls = [20, 9]
        expected_damage = [4]
        expected_armor = [5]

        metadata = simulate_attack(event,
                                   die_rolls,
                                   weapon_def=self.weapon_def,
                                   target_def=self.target_sanctified_armor_def)

        actual_damage = metadata[EFFECTIVE_DAMAGE]
        actual_armor = metadata[EFFECTIVE_ARMOR]

        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_armor, actual_armor)
