from unittest import TestCase

from src.cli.quick_dict import quick_dict_parse


class Test(TestCase):

    def setUp(self):
        self.match_map = {'fruits': ['banana', 'melon', 'avocado'],
                          'people': ['hank', 'james', 'the_emperor'],
                          'food': ['bacon', 'ham', 'eggs'],
                          'criminals': None}

    def test_empty_string_should_return_empty_dict(self):
        input_string = ''
        expected = {}
        actual = quick_dict_parse(input_string)
        self.assertEqual(expected, actual)

    def test_single_key_value_no_whitespace_should_return_dict_with_same_key_value(self):
        input_string = 'KEY:VALUE'
        expected = {'key': 'value'}
        actual = quick_dict_parse(input_string)
        self.assertEqual(expected, actual)

    def test_two_key_values_no_whitespace_should_return_dict_with_same_key_values(self):
        input_string = 'KEY_1:VALUE,KEY_2:VALUE'
        expected = {'key_1': 'value',
                    'key_2': 'value'}
        actual = quick_dict_parse(input_string)
        self.assertEqual(expected, actual)

    def test_single_key_value_with_whitespace_should_return_dict_without_whitespace(self):
        input_string = '''        KEY     :     VALUE     '''
        expected = {'key': 'value'}
        actual = quick_dict_parse(input_string)
        self.assertEqual(expected, actual)

    def test_incorrect_pair_syntax_should_ignore_that_pair_but_not_other_pairs(self):
        input_string = 'KEY_1VALUE, KEY_2:VALUE'
        expected = {'key_2': 'value'}
        actual = quick_dict_parse(input_string)
        self.assertEqual(expected, actual)

    def test_match_map_should_adjust_to_close_matches(self):
        input_string = 'frts: banena, poeple: emperar, food: bcon'
        expected = {'fruits': 'banana',
                    'people': 'the_emperor',
                    'food': 'bacon'}
        actual = quick_dict_parse(input_string, match_map=self.match_map)
        self.assertEqual(expected, actual)

    def test_pair_with_no_match_should_not_be_allowed(self):
        input_string = 'people: the emperor, other: BBB'
        expected = {'people': 'the_emperor'}
        actual = quick_dict_parse(input_string, match_map=self.match_map)
        self.assertEqual(expected, actual)

    def test_pair_with_half_match_should_not_be_allowed(self):
        input_string = 'people: AAAAAAAAAAAAA'
        expected = {}
        actual = quick_dict_parse(input_string, match_map=self.match_map)
        self.assertEqual(expected, actual)

    def test_pair_with_matches_none_should_allow_anything(self):
        input_string = 'criminals: AAAA'
        expected = {'criminals': 'aaaa'}
        actual = quick_dict_parse(input_string, match_map=self.match_map)
        self.assertEqual(expected, actual)
