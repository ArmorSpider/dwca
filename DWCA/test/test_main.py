import unittest

from hypothesis import strategies as st
from hypothesis.core import given

from src.dice.dice import DummyDice
from src.dice.dice_pool import DicePool
from src.goal_roll.goal_roll import GoalRoll


class Test(unittest.TestCase):

    def test_roll_dice_should_return_list_of_results(self):
        expected = [1, 2, 3, 4]
        dice_list = [
            DummyDice(4),
            DummyDice(2),
            DummyDice(3),
            DummyDice(1)
        ]
        dice_pool = DicePool(dice_list)
        actual = dice_pool._roll_dice()

        self.assert_lists_equal(expected, actual)

    def test_roll_should_return_total_result(self):
        expected = 1 + 2 + 3 + 4
        dice_list = [
            DummyDice(4),
            DummyDice(2),
            DummyDice(3),
            DummyDice(1)
        ]
        dice_pool = DicePool(dice_list)
        actual = dice_pool.roll()

        self.assertEqual(expected, actual)

    @given(_roll_dice=st.integers(min_value=1, max_value=100), target=st.integers(min_value=1, max_value=300))
    def test_get_degrees_of_success_should_work(self, _roll_dice, target):
        goal_roll = GoalRoll(_roll_dice, target)
        dos = goal_roll.get_degrees_of_success()
        self.assert_dos_calculation(goal_roll, dos)

    def assert_dos_calculation(self, goal_roll, dos):
        _roll_dice = goal_roll._roll_dice
        target = goal_roll.target
        diff = target - _roll_dice
        tens = int(diff / 10)
        if tens < 0:
            tens = 0
        # print 'Roll: {}, Target: {}, Diff:{} , DoS: {}'.format(_roll_dice, target,
        # diff, dos)
        self.assertTrue(dos <= tens)

    def assert_lists_equal(self, expected, actual):
        self.assertEqual(sorted(expected), sorted(actual))
