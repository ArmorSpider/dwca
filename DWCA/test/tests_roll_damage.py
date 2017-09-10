import unittest
from src.roll_damage import handle_dos_minimum_damage


class Test(unittest.TestCase):

    def test_a_single_dice_should_be_modified_by_dos(self):
        roll_results = [9, 5, 1]
        dos = 6
        expected = [9, 6, 5]
        actual = handle_dos_minimum_damage(dos, roll_results)
        self.assertEqual(expected, actual)
