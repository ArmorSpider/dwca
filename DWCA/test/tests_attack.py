
# pylint: skip-file

import unittest

from src.action.attack import Attack
from src.entities import NAME, DAMAGE, PENETRATION, DICE, QUALITIES, TALENTS,\
    TRAITS, ARMOR, CHARACTERISTICS
from src.entities.character import Character
from src.entities.weapon import Weapon
from src.hit_location import HITLOC_ALL, HITLOC_BODY


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
        actual = _melee_attack.get_weapon()

        self.assertEqual(expected, actual)

    def test_attack_should_contain_attacker(self):
        entity = self.entity
        weapon = self.weapon
        _melee_attack = entity._melee_attack(weapon=weapon)

        expected = entity
        actual = _melee_attack.get_attacker()

        self.assertEqual(expected, actual)

    def test_attack_should_contain_target_if_specified(self):
        entity = self.entity
        weapon = self.weapon
        _melee_attack = entity._melee_attack(weapon=weapon, target=entity)

        expected = entity
        actual = _melee_attack.get_target()

        self.assertEqual(expected, actual)

    def test_get_qualities_should_return_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = {'balanced': True, 'tearing': True}
        actual = _melee_attack.get_weapon_stat(QUALITIES)

        self.assertEqual(expected, actual)

    def test_get_attacker_traits_should_return_attacker_traits(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = {'machine': 5}
        actual = _melee_attack.get_attacker_stat(TRAITS)

        self.assertEqual(expected, actual)

    def test_get_attacker_talents_should_return_attacker_talents(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = {'crushing_blow': True}
        actual = _melee_attack.get_attacker_stat(TALENTS)

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
        actual = _melee_attack._calculate_num_dice()

        self.assertEqual(expected, actual)

    def test_calculate_penetration_should_use_weapons_penetration(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = 3
        actual = _melee_attack._calculate_penetration()

        self.assertEqual(expected, actual)

    def test_calculate_flat_damage_should_use_weapons_damage(self):
        entity = self.space_marine
        weapon = self.chainsword
        _melee_attack = entity._melee_attack(weapon)

        expected = 5
        actual = _melee_attack._calculate_flat_damage()

        self.assertEqual(expected, actual)
