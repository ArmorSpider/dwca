import unittest

from definitions import PROTECTION_MAX, OVERLOAD_MAX
from src.situational.force_field import ForceField


class Test(unittest.TestCase):

    def setUp(self):
        self.force_field = ForceField({PROTECTION_MAX: 25, OVERLOAD_MAX: 10})

    def test_above_protection_max_should_hit(self):
        self.assertFalse(self.force_field.is_hit_blocked(26))

    def test_below_or_equal_protection_max_should_be_blocked(self):
        self.assertTrue(self.force_field.is_hit_blocked(25))

    def test_overload_should_block_hit(self):
        self.assertTrue(self.force_field.is_hit_blocked(1))

    def test_after_overload_anything_should_hit(self):
        self.assertTrue(self.force_field.is_hit_blocked(25))
        self.assertTrue(self.force_field.is_hit_blocked(1))
        self.assertFalse(self.force_field.is_hit_blocked(25))
