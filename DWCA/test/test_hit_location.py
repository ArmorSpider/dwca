
import unittest

from src.hit_location import HitLocation, get_hit_location, RIGHT_ARM, BODY,\
    HEAD, LEFT_ARM, LEFT_LEG, RIGHT_LEG
from src.hitloc_series import get_hit_locations


class Test(unittest.TestCase):

    def test_get_hit_location_should_work(self):
        input_rolls = [10, 20, 30, 70, 85, 100]
        expected_locations = [HitLocation.HEAD,
                              HitLocation.RIGHT_ARM,
                              HitLocation.LEFT_ARM,
                              HitLocation.BODY,
                              HitLocation.RIGHT_LEG,
                              HitLocation.LEFT_LEG]

        for input_roll, expected_location in zip(input_rolls, expected_locations):
            actual = get_hit_location(input_roll)
            self.assertEqual(expected_location, actual)

    def test_non_matching_hit_location_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            get_hit_location(9000)

    def test_get_hit_locations_for_right_arm_should_match_expectations(self):
        expected = [RIGHT_ARM, RIGHT_ARM, BODY, HEAD,
                    BODY,  RIGHT_ARM, RIGHT_ARM, RIGHT_ARM]
        actual = get_hit_locations(HitLocation.RIGHT_ARM, len(expected))
        self.assertEqual(expected, actual)

    def test_get_hit_locations_for_left_arm_should_match_expectations(self):
        expected = [LEFT_ARM, LEFT_ARM, BODY, HEAD,
                    BODY,  LEFT_ARM, LEFT_ARM, LEFT_ARM]
        actual = get_hit_locations(HitLocation.LEFT_ARM, len(expected))
        self.assertEqual(expected, actual)

    def test_get_hit_locations_for_left_leg_should_match_expectations(self):
        expected = [LEFT_LEG, LEFT_LEG, BODY, LEFT_ARM,
                    HEAD, BODY, BODY, BODY]
        actual = get_hit_locations(HitLocation.LEFT_LEG, len(expected))
        self.assertEqual(expected, actual)

    def test_get_hit_locations_for_right_leg_should_match_expectations(self):
        expected = [RIGHT_LEG, RIGHT_LEG, BODY, RIGHT_ARM,
                    HEAD, BODY, BODY, BODY]
        actual = get_hit_locations(HitLocation.RIGHT_LEG, len(expected))
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
