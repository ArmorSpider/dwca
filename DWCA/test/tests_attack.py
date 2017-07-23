'''
Created on 5 Jul 2017

@author: Dos'
'''
import unittest

from src.action.attack import Attack
from src.entities import NAME, DAMAGE, PENETRATION, DICE, QUALITIES, TALENTS,\
    TRAITS, ARMOR
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
        melee_attack = entity.melee_attack(weapon)

        self.assertIsInstance(melee_attack, Attack)

    def test_attack_should_contain_weapon(self):
        entity = self.entity
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = weapon
        actual = melee_attack.get_weapon()

        self.assertEqual(expected, actual)

    def test_attack_should_contain_attacker(self):
        entity = self.entity
        weapon = self.weapon
        melee_attack = entity.melee_attack(weapon=weapon)

        expected = entity
        actual = melee_attack.get_attacker()

        self.assertEqual(expected, actual)

    def test_attack_should_contain_target_if_specified(self):
        entity = self.entity
        weapon = self.weapon
        melee_attack = entity.melee_attack(weapon=weapon, target=entity)

        expected = entity
        actual = melee_attack.get_target()

        self.assertEqual(expected, actual)

    def test_get_qualities_should_return_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = {'balanced': True, 'tearing': True}
        actual = melee_attack._get_weapon_qualities()

        self.assertEqual(expected, actual)

    def test_get_attacker_traits_should_return_attacker_traits(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = {'machine': 5}
        actual = melee_attack._get_attacker_traits()

        self.assertEqual(expected, actual)

    def test_get_attacker_talents_should_return_attacker_talents(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = {'crushing_blow': True}
        actual = melee_attack._get_attacker_talents()

        self.assertEqual(expected, actual)

    def test_get_offensive_modifiers_should_return_attacker_traits_talents_and_weapon_qualities(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = {'crushing_blow': True,
                    'machine': 5,
                    'balanced': True,
                    'tearing': True}
        actual = melee_attack._combine_offensive_modifiers()

        self.assertEqual(expected, actual)

    def test_get_defensive_modifiers_should_return_target_traits_and_talents(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon, target=entity)

        expected = {'crushing_blow': True,
                    'machine': 5}
        actual = melee_attack._combine_defensive_modifiers()

        self.assertEqual(expected, actual)

    def test_calculate_num_damage_dice_should_use_weapons_num_dice(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = 1
        actual = melee_attack.calculate_num_dice()

        self.assertEqual(expected, actual)

    def test_calculate_penetration_should_use_weapons_penetration(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = 3
        actual = melee_attack.calculate_penetration()

        self.assertEqual(expected, actual)

    def test_calculate_flat_damage_should_use_weapons_damage(self):
        entity = self.space_marine
        weapon = self.chainsword
        melee_attack = entity.melee_attack(weapon)

        expected = 5
        actual = melee_attack.calculate_flat_damage()

        self.assertEqual(expected, actual)
