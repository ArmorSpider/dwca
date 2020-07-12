import unittest

from src.entities.char_stats import STAT_WS, STAT_BS, STAT_STR, STAT_TGH,\
    STAT_AGI, STAT_PER, STAT_WIL, STAT_FEL, STAT_INT
from src.entities.entity_factory import build_entity
from src.skills import BasicSkills
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
        self.basic_skills = {'acrobatics': 0,
                             'athletics': 0,
                             'awareness': 0,
                             'charm': 0,
                             'command': 0,
                             'commerce': 0,
                             'lore_common': 0,
                             'deceive': 0,
                             'dodge': 0,
                             'lore_forbidden': 0,
                             'inquiry': 0,
                             'interrogation': 0,
                             'intimidate': 0,
                             'linguistics': 0,
                             'logic': 0,
                             'medicae': 0,
                             'navigate': 0,
                             'operate': 0,
                             'parry': 0,
                             'psyniscience': 0,
                             'lore_scholastic': 0,
                             'scrutiny': 0,
                             'security': 0,
                             'sleight_of_hand': 0,
                             'stealth': 0,
                             'survival': 0,
                             'tech_use': 0,
                             'trade': 0}
        self.odd_basic_skills = {'acrobatics': 1,
                                 'athletics': 2,
                                 'awareness': 3,
                                 'charm': 4,
                                 'command': 5,
                                 'commerce': 6,
                                 'lore_common': 7,
                                 'deceive': 8,
                                 'dodge': 9,
                                 'lore_forbidden': 10,
                                 'inquiry': 11,
                                 'interrogation': 12,
                                 'intimidate': 13,
                                 'linguistics': 14,
                                 'logic': 15,
                                 'medicae': 16,
                                 'navigate': 17,
                                 'operate': 18,
                                 'parry': 19,
                                 'psyniscience': 20,
                                 'lore_scholastic': 21,
                                 'scrutiny': 22,
                                 'security': 23,
                                 'sleight_of_hand': 24,
                                 'stealth': 25,
                                 'survival': 26,
                                 'tech_use': 27,
                                 'trade': 28}

    def test_no_configured_skills_should_return_basic_skills_with_penalty(self):
        expected = {skill.value: 20 for skill in BasicSkills}
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics)

    def test_skills_should_use_the_correct_characteristic_value(self):
        agi = 50 - 20
        per = 60 - 20
        str_ = 30 - 20
        int_ = 90 - 20
        wil = 70 - 20
        fel = 80 - 20
        ws = 10 - 20
        expected = {'acrobatics': agi,
                    'athletics': str_,
                    'awareness': per,
                    'charm': fel,
                    'command': fel,
                    'commerce': int_,
                    'lore_common': int_,
                    'deceive': fel,
                    'dodge': agi,
                    'lore_forbidden': int_,
                    'inquiry': fel,
                    'interrogation': wil,
                    'intimidate': str_,
                    'linguistics': int_,
                    'logic': int_,
                    'medicae': int_,
                    'navigate': int_,
                    'operate': agi,
                    'parry': ws,
                    'psyniscience': per,
                    'lore_scholastic': int_,
                    'scrutiny': per,
                    'security': int_,
                    'sleight_of_hand': agi,
                    'stealth': agi,
                    'survival': per,
                    'tech_use': int_,
                    'trade': int_}
        self.assert_available_skills(expected,
                                     characteristics=self.odd_characteristics)

    def test_trained_basic_skills_should_use_full_characteristic(self):
        expected = {skill.value: 40 for skill in BasicSkills}
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics,
                                     skills=self.basic_skills)

    def test_trained_skills_should_use_each_unique_skill_training_rating(self):
        expected = {'acrobatics': 40 + 1,
                    'athletics': 40 + 2,
                    'awareness': 40 + 3,
                    'charm': 40 + 4,
                    'command': 40 + 5,
                    'commerce': 40 + 6,
                    'lore_common': 40 + 7,
                    'deceive': 40 + 8,
                    'dodge': 40 + 9,
                    'lore_forbidden': 40 + 10,
                    'inquiry': 40 + 11,
                    'interrogation': 40 + 12,
                    'intimidate': 40 + 13,
                    'linguistics': 40 + 14,
                    'logic': 40 + 15,
                    'medicae': 40 + 16,
                    'navigate': 40 + 17,
                    'operate': 40 + 18,
                    'parry': 40 + 19,
                    'psyniscience': 40 + 20,
                    'lore_scholastic': 40 + 21,
                    'scrutiny': 40 + 22,
                    'security': 40 + 23,
                    'sleight_of_hand': 40 + 24,
                    'stealth': 40 + 25,
                    'survival': 40 + 26,
                    'tech_use': 40 + 27,
                    'trade': 40 + 28}
        self.assert_available_skills(expected,
                                     characteristics=self.even_characteristics,
                                     skills=self.odd_basic_skills)

    def assert_available_skills(self, expected, characteristics={}, skills={}):
        entity_name = add_mock_entity('MockMan', characteristics=characteristics,
                                      skills=skills)
        entity = build_entity(entity_name)
        actual = entity.available_skills
        self.assertEqual(expected, actual)
