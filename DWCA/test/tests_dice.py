
import unittest
from src.dice import queue_rolls, roll_damage_dice


class Test(unittest.TestCase):

    def test_queued_rolls_should_be_returned_in_order(self):
        queued_rolls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        queue_rolls(queued_rolls)
        expected = queued_rolls
        actual = roll_damage_dice(10)
        self.assertEqual(actual, expected)

    def test_queueing_rolls_should_remove_previously_queued_rolls(self):
        queue_rolls([5000, 7000, 35])
        queued_rolls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        queue_rolls(queued_rolls)
        expected = queued_rolls
        actual = roll_damage_dice(10)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
