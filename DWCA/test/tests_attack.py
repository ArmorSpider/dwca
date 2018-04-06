
# pylint: skip-file

import unittest

from src.action.attack import Attack
from src.entities import NAME, FLAT_DAMAGE, PENETRATION, DICE, QUALITIES, TALENTS,\
    TRAITS, ARMOR, CHARACTERISTICS
from src.entities.char_stats import STAT_STR, STAT_WS
from src.entities.character import Character
from src.entities.weapon import Weapon
from src.hit_location import HITLOC_ALL, HITLOC_BODY
from test.test_util import build_mock_weapon, build_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        self.entity = Character()
        self.weapon = Weapon()
        chainsword_definition = {
            NAME: 'Astartes Chainsword',
            FLAT_DAMAGE: 5,
            PENETRATION: 3,
            DICE: 1,
            QUALITIES: {
                'balanced': True,
                'tearing': True
            }
        }
        space_marine_definition = {
            NAME: 'Space Marine',
            CHARACTERISTICS: {},
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

        self.weak_attacker = build_mock_entity('WeakMan',
                                               _system='deathwatch',
                                               characteristics={STAT_STR: 10,
                                                                STAT_WS: 50,
                                                                STAT_STR + '_bonus': 20})
        self.weapon_with_stats = build_mock_weapon('StatBlade',
                                                   'Melee',
                                                   _system='deathwatch',
                                                   characteristics={STAT_STR: 85,
                                                                    STAT_WS + '_bonus': 15})

    def test_attacking_should_return_an_attack(self):
        entity = self.entity
        weapon = self.weapon
        _melee_attack = entity._melee_attack(weapon)

        self.assertIsInstance(_melee_attack, Attack)

    def test_attack_should_contain_weapon(self):
        entity = self.entity
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = weapon
        actual = _melee_attack.weapon

        self.assertEqual(expected, actual)

    def test_attack_should_contain_attacker(self):
        entity = self.entity
        weapon = self.weapon
        _melee_attack = entity._melee_attack(weapon=weapon)

        expected = entity
        actual = _melee_attack.attacker

        self.assertEqual(expected, actual)

    def test_attack_should_contain_target_if_specified(self):
        entity = self.entity
        weapon = self.weapon
        _melee_attack = entity._melee_attack(weapon=weapon, target=entity)

        expected = entity
        actual = _melee_attack.target

        self.assertEqual(expected, actual)

    def test_get_qualities_should_return_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = {'balanced': True, 'tearing': True}
        actual = _melee_attack.weapon.qualities

        self.assertEqual(expected, actual)

    def test_get_attacker_traits_should_return_attacker_traits(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = {'machine': 5}
        actual = _melee_attack.attacker.traits

        self.assertEqual(expected, actual)

    def test_get_attacker_talents_should_return_attacker_talents(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = {'crushing_blow': True}
        actual = _melee_attack.attacker.talents

        self.assertEqual(expected, actual)

    def test_get_offensive_modifiers_should_return_attacker_traits_talents_and_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = {'crushing_blow': True,
                    'machine': 5,
                    'balanced': True,
                    'tearing': True}
        actual = _melee_attack.offensive_modifiers

        self.assertEqual(expected, actual)

    def test_calculate_num_damage_dice_should_use_weapons_num_dice(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = 1
        actual = _melee_attack.num_dice

        self.assertEqual(expected, actual)

    def test_calculate_penetration_should_use_weapons_penetration(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = 3
        actual = _melee_attack.penetration

        self.assertEqual(expected, actual)

    def test_calculate_flat_damage_should_use_weapons_damage(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = 5
        actual = _melee_attack.weapon.flat_damage

        self.assertEqual(expected, actual)

    def test_get_attr_should_lookup_in_offensive_modifiers(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)
        self.assertEqual(True, _melee_attack.crushing_blow)
        self.assertEqual(5, _melee_attack.machine)
        self.assertEqual(True, _melee_attack.balanced)
        self.assertEqual(True, _melee_attack.tearing)

    def test_weapon_characteristic_should_override_attacker_including_flat_bonus(self):
        attack = Attack(weapon=self.weapon_with_stats,
                        attacker=self.weak_attacker,
                        target=None)
        expected = 85
        expected_bonus = 8
        actual = attack.get_effective_characteristic(STAT_STR)
        actual_bonus = attack.get_effective_bonus(STAT_STR)

        self.assertEqual(expected, actual)
        self.assertEqual(expected_bonus, actual_bonus)

    def test_attacker_characteristic_should_include_bonus_from_weapon(self):
        attack = Attack(weapon=self.weapon_with_stats,
                        attacker=self.weak_attacker,
                        target=None)
        expected = 65
        expected_bonus = 6
        actual = attack.get_effective_characteristic(STAT_WS)
        actual_bonus = attack.get_effective_bonus(STAT_WS)

        self.assertEqual(expected, actual)
        self.assertEqual(expected_bonus, actual_bonus)
