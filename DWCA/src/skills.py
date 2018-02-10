from enum import Enum

from src.entities.char_stats import STAT_STR, STAT_PER, STAT_FEL,\
    STAT_AGI, STAT_WIL, STAT_INT, STAT_WS


def get_all_skills():
    all_skills = get_basic_skills()
    return all_skills


def get_basic_skills():
    basic_skills = [skill.value for skill in BasicSkills]
    return basic_skills


class BasicSkills(Enum):
    ACROBATICS = 'acrobatics'
    ATHLETICS = 'athletics'
    AWARENESS = 'awareness'
    CHARM = 'charm'
    COMMAND = 'command'
    COMMERCE = 'commerce'
    LORE_COMMON = 'lore_common'
    DECEIVE = 'deceive'
    DODGE = 'dodge'
    LORE_FORBIDDEN = 'lore_forbidden'
    INQUIRY = 'inquiry'
    INTERROGATION = 'interrogation'
    INTIMIDATE = 'intimidate'
    LINGUISTICS = 'linguistics'
    LOGIC = 'logic'
    MEDICAE = 'medicae'
    NAVIGATE = 'navigate'
    OPERATE = 'operate'
    PARRY = 'parry'
    PSYNISCIENCE = 'psyniscience'
    LORE_SCHOLASTIC = 'lore_scholastic'
    SCRUTINY = 'scrutiny'
    SECURITY = 'security'
    SLEIGHT_OF_HAND = 'sleight_of_hand'
    STEALTH = 'stealth'
    SURVIVAL = 'survival'
    TECH_USE = 'tech_use'
    TRADE = 'trade'


def get_skill_characteristic(active_skill):
    for char_stat, skills in get_skill_characteristic_mappings().iteritems():
        for skill in skills:
            if active_skill.lower() == skill.value:
                return char_stat
    return None


def get_skill_characteristic_mappings():
    return {STAT_STR: (BasicSkills.ATHLETICS,
                       BasicSkills.INTIMIDATE),
            STAT_PER: (BasicSkills.AWARENESS,
                       BasicSkills.SCRUTINY,
                       BasicSkills.PSYNISCIENCE,
                       BasicSkills.SURVIVAL),
            STAT_FEL: (BasicSkills.CHARM,
                       BasicSkills.COMMAND,
                       BasicSkills.DECEIVE,
                       BasicSkills.INQUIRY),
            STAT_AGI: (BasicSkills.DODGE,
                       BasicSkills.STEALTH,
                       BasicSkills.ACROBATICS,
                       BasicSkills.SLEIGHT_OF_HAND,
                       BasicSkills.OPERATE),
            STAT_WIL: (BasicSkills.INTERROGATION,),
            STAT_INT: (BasicSkills.COMMERCE,
                       BasicSkills.LINGUISTICS,
                       BasicSkills.LOGIC,
                       BasicSkills.LORE_COMMON,
                       BasicSkills.LORE_FORBIDDEN,
                       BasicSkills.LORE_SCHOLASTIC,
                       BasicSkills.SECURITY,
                       BasicSkills.TECH_USE,
                       BasicSkills.TRADE,
                       BasicSkills.MEDICAE,
                       BasicSkills.NAVIGATE),
            STAT_WS: (BasicSkills.PARRY,)}
