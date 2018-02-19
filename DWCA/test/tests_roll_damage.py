import unittest

from src.action.action import Action
from src.roll_damage import handle_dos_minimum_damage


class Test(unittest.TestCase):

    def test_a_single_dice_should_be_modified_by_dos(self):
        roll_results = [9, 5, 1]
        attack = Action()
        attack.roll_result = 1
        attack.roll_target = 61
        expected = [9, 7, 5]
        actual = handle_dos_minimum_damage(attack, roll_results)
        self.assertEqual(expected, actual)
