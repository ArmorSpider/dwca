import unittest

from hypothesis import strategies as st
from hypothesis.core import given
from src.action.action import Action


class Test(unittest.TestCase):

    @given(result=st.integers(min_value=1, max_value=100), roll_target=st.integers(min_value=1, max_value=300))
    def test_get_degrees_of_success_should_work(self, result, roll_target):
        action = Action()
        action.try_action(roll_target, result)
        dos = action.get_degrees_of_success()
        self.assert_dos_calculation(action, dos)

    def test_get_reverse_should_reverse_roll_result(self):
        input_values = [21, 100, 20, 1]
        expected = [12, 001, 02, 10]

        for input_value, expected_value in zip(input_values, expected):
            action = Action()
            action.try_action(100, roll_result=input_value)
            actual = action.get_reverse()
            self.assertEqual(expected_value, actual)

    def assert_dos_calculation(self, action, dos):
        roll_result = action.roll_result
        roll_target = action.roll_target
        diff = roll_target - roll_result
        tens = int(diff / 10)
        if tens < 0:
            tens = 0
        # print 'Roll: {}, Target: {}, Diff:{} , DoS: {}'.format(roll_result, roll_target,
        # diff, dos)
        self.assertTrue(dos <= tens)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
