
import unittest

from src.modifiers.modifier import register_modifiers
from src.entities.character import get_char
from src.entities.weapon import get_weapon


class Test(unittest.TestCase):

    def setUp(self):
        register_modifiers()

    def test_genestealer(self):
        entity = get_char('auran_genestealer')
        weapon = get_weapon('rending_claws')
        attack = entity.melee_attack(weapon, entity)
        attack.try_action(96, 1)
        expected_dice = 1
        expected_pen = 10
        expected_damage = 14
        expected_dos = 9

        actual_dice = attack.calculate_num_dice()
        actual_pen = attack.calculate_penetration()
        actual_damage = attack.calculate_flat_damage()
        actual_dos = attack.get_degrees_of_success()

        self.assertEqual(expected_dice, actual_dice)
        self.assertEqual(expected_pen, actual_pen)
        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_dos, actual_dos)
