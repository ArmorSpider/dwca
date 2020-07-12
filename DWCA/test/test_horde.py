import unittest

from src.entities.entity_factory import build_entity
from test.test_util import add_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        self.hulking_person = add_mock_entity(
            'Hulking Person', traits={'size': 10})

    def test_magnitude_below_30_should_return_standard_size_bonus(self):
        horde = build_entity(self.hulking_person, 10)
        expected = 10
        actual = horde.size_bonus
        self.assertEqual(expected, actual)

    def test_magnitude_30_should_add_plus_30(self):
        horde = build_entity(self.hulking_person, 30)
        expected = 40
        actual = horde.size_bonus
        self.assertEqual(expected, actual)

    def test_magnitude_above_60_should_add_plus_40(self):
        horde = build_entity(self.hulking_person, 60)
        expected = 50
        actual = horde.size_bonus
        self.assertEqual(expected, actual)

    def test_magnitude_above_90_should_add_plus_50(self):
        horde = build_entity(self.hulking_person, 90)
        expected = 60
        actual = horde.size_bonus
        self.assertEqual(expected, actual)

    def test_magnitude_above_120_should_add_plus_60(self):
        horde = build_entity(self.hulking_person, 120)
        expected = 70
        actual = horde.size_bonus
        self.assertEqual(expected, actual)
