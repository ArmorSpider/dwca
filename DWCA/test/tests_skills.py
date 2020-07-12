import unittest

from src.entities.char_stats import STAT_WS, STAT_BS, STAT_STR, STAT_TGH,\
    STAT_AGI, STAT_PER, STAT_WIL, STAT_FEL, STAT_INT
from src.entities.entity_factory import build_entity
from src.skills import BasicSkills, AdvancedSkills
from test.test_util import add_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.even_characteristics = {STAT_WS: 40,
                                     STAT_BS: 40,
                                     STAT_STR: 40,
                                     STAT_TGH: 40,
                                     STAT_AGI: 40,
                                     STAT_PER: 40,
                                     STAT_WIL: 40,
                                     STAT_FEL: 40,
                                     STAT_INT: 40}
        self.odd_characteristics = {STAT_WS: 10,
                                    STAT_BS: 20,
                                    STAT_STR: 30,
                                    STAT_TGH: 40,
                                    STAT_AGI: 50,
                                    STAT_PER: 60,
                                    STAT_WIL: 70,
                                    STAT_FEL: 80,
                                    STAT_INT: 90}
        self.basic_skills = {'dodge': 0,
                             'carouse': 0,
                             'search': 0,
                             'silent_move': 0,
                             'intimidate': 0,
                             'evaluate': 0,
                             'inquiry': 0,
                             'scrutiny': 0,
                             'charm': 0,
                             'gamble': 0,
                             'deceive': 0,
                             'logic': 0,
                             'swim': 0,
                             'command': 0,
                             'climb': 0,
                             'concealment': 0,
                             'contortionist': 0,
                             'awareness': 0}
        self.odd_basic_skills = {'dodge': 1,
                                 'carouse': 2,
                                 'search': 3,
                                 'silent_move': 4,
                                 'intimidate': 5,
                                 'evaluate': 6,
                                 'inquiry': 7,
                                 'scrutiny': 8,
                                 'charm': 9,
                                 'gamble': 10,
                                 'deceive': 11,
                                 'logic': 12,
                                 'swim': 13,
                                 'command': 14,
                                 'climb': 15,
                                 'concealment': 16,
                                 'contortionist': 17,
                                 'awareness': 18}
        self.advanced_skills = {'performer': 0,
                                'psyniscience': 0,
                                'tracking': 0,
                                'chem_use': 0,
                                'demolition': 0,
                                'shadowing': 0,
                                'tech_use': 0,
                                'literacy': 0,
                                'invocation': 0,
                                'acrobatics': 0,
                                'wrangling': 0,
                                'survival': 0,
                                'ciphers': 0,
                                'lore_scholastic': 0,
                                'interrogation': 0,
                                'medicae': 0,
                                'lip_reading': 0,
                                'trade': 0,
                                'pilot': 0,
                                'lore_common': 0,
                                'tactics': 0,
                                'sleight_of_hand': 0,
                                'lore_forbidden': 0,
                                'drive': 0,
                                'speak_language': 0,
                                'security': 0,
                                'navigation': 0}
        self.odd_advanced_skills = {'performer': 1,
                                    'psyniscience': 2,
                                    'tracking': 3,
                                    'chem_use': 4,
                                    'demolition': 5,
                                    'shadowing': 6,
                                    'tech_use': 7,
                                    'literacy': 8,
                                    'invocation': 9,
                                    'acrobatics': 10,
                                    'wrangling': 11,
                                    'survival': 12,
                                    'ciphers': 13,
                                    'lore_scholastic': 14,
                                    'interrogation': 15,
                                    'medicae': 16,
                                    'lip_reading': 17,
                                    'trade': 18,
                                    'pilot': 19,
                                    'lore_common': 20,
                                    'tactics': 21,
                                    'sleight_of_hand': 22,
                                    'lore_forbidden': 23,
                                    'drive': 24,
                                    'speak_language': 25,
                                    'security': 26,
                                    'navigation': 27}

    def test_no_configured_skills_should_return_basic_skills_with_halved_characteristics(self):
        expected = {skill.value: 20 for skill in BasicSkills}
        print({skill.value: 0 for skill in AdvancedSkills})
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics)

    def test_skills_should_use_the_correct_characteristic_value(self):
        agi = 25
        tgh = 20
        per = 30
        str_ = 15
        int_ = 45
        fel = 40
        expected = {'dodge': agi,
                    'carouse': tgh,
                    'search': per,
                    'silent_move': agi,
                    'intimidate': str_,
                    'evaluate': int_,
                    'inquiry': fel,
                    'scrutiny': per,
                    'charm': fel,
                    'gamble': per,
                    'deceive': fel,
                    'logic': int_,
                    'swim': str_,
                    'command': fel,
                    'climb': str_,
                    'concealment': agi,
                    'contortionist': agi,
                    'awareness': per}
        self.assert_available_skills(expected,
                                     characteristics=self.odd_characteristics)

    def test_trained_basic_skills_should_use_full_characteristic(self):
        expected = {skill.value: 40 for skill in BasicSkills}
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics,
                                     skills=self.basic_skills)

    def test_trained_skills_should_use_each_unique_skill_training_rating(self):
        expected = {'dodge': 40 + 1,
                    'carouse': 40 + 2,
                    'search': 40 + 3,
                    'silent_move': 40 + 4,
                    'intimidate': 40 + 5,
                    'evaluate': 40 + 6,
                    'inquiry': 40 + 7,
                    'scrutiny': 40 + 8,
                    'charm': 40 + 9,
                    'gamble': 40 + 10,
                    'deceive': 40 + 11,
                    'logic': 40 + 12,
                    'swim': 40 + 13,
                    'command': 40 + 14,
                    'climb': 40 + 15,
                    'concealment': 40 + 16,
                    'contortionist': 40 + 17,
                    'awareness': 40 + 18}
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics,
                                     skills=self.odd_basic_skills)

    def test_advanced_skills_should_be_returned_if_trained(self):
        expected = {skill.value: 40 for skill in list(
            BasicSkills) + list(AdvancedSkills)}
        skills = {}
        skills.update(self.advanced_skills)
        skills.update(self.basic_skills)
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics,
                                     skills=skills)

    def test_advanced_skills_should_use_unique_skill_value_for_each_skill(self):
        skills = {}
        skills.update(self.odd_advanced_skills)
        skills.update(self.basic_skills)
        expected = {'performer': 40 + 1,
                    'psyniscience': 40 + 2,
                    'tracking': 40 + 3,
                    'chem_use': 40 + 4,
                    'demolition': 40 + 5,
                    'shadowing': 40 + 6,
                    'tech_use': 40 + 7,
                    'literacy': 40 + 8,
                    'invocation': 40 + 9,
                    'acrobatics': 40 + 10,
                    'wrangling': 40 + 11,
                    'survival': 40 + 12,
                    'ciphers': 40 + 13,
                    'lore_scholastic': 40 + 14,
                    'interrogation': 40 + 15,
                    'medicae': 40 + 16,
                    'lip_reading': 40 + 17,
                    'trade': 40 + 18,
                    'pilot': 40 + 19,
                    'lore_common': 40 + 20,
                    'tactics': 40 + 21,
                    'sleight_of_hand': 40 + 22,
                    'lore_forbidden': 40 + 23,
                    'drive': 40 + 24,
                    'speak_language': 40 + 25,
                    'security': 40 + 26,
                    'navigation': 40 + 27}
        expected.update({skill.value: 40 for skill in BasicSkills})
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics,
                                     skills=skills)

    def assert_available_skills(self, expected, characteristics={}, skills={}):
        entity_name = add_mock_entity('MockMan', characteristics=characteristics,
                                      skills=skills)
        entity = build_entity(entity_name)
        actual = entity.available_skills
        self.assertEqual(expected, actual)
