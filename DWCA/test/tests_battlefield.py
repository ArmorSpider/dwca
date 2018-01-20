import unittest

from src.battlefield.battlefield import Group
from test.test_util import add_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        self.nice_name = 'SpaceMarine'
        self.space_marine_name = add_mock_entity(self.nice_name, wounds=10)

    def tearDown(self):
        pass

    def test_a_single_space_marine_should_return_without_index(self):
        group = Group()
        group.add(self.space_marine_name)
        expected = {self.nice_name: {'wounds': 10}}
        actual = group.frontend
        self.assertEqual(expected, actual)

    def test_two_space_marines_should_return_with_index(self):
        group = Group()
        group.add(self.space_marine_name)
        group.add(self.space_marine_name)
        expected = {self.nice_name + '_1': {'wounds': 10},
                    self.nice_name + '_2': {'wounds': 10}}
        actual = group.frontend
        self.assertEqual(expected, actual)

    def test_two_remove_one_should_return_without_index(self):
        group = Group()
        group.add(self.space_marine_name)
        group.add(self.space_marine_name)
        group.remove(self.space_marine_name)
        expected = {self.nice_name: {'wounds': 10}}
        actual = group.frontend
        self.assertEqual(expected, actual)

    def test_three_remove_number_two_should_return_one_and_three(self):
        group = Group()
        group.add(self.space_marine_name)
        group.add(self.space_marine_name)
        group.add(self.space_marine_name)
        group.remove(self.space_marine_name, 1)
        expected = {self.nice_name + '_1': {'wounds': 10},
                    self.nice_name + '_3': {'wounds': 10}}
        actual = group.frontend
        self.assertEqual(expected, actual)
