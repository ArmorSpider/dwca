from enum import Enum

from src.entities.char_stats import STAT_STR, STAT_PER, STAT_TGH, STAT_FEL,\
    STAT_AGI, STAT_WIL, STAT_INT


def get_all_skills():
    all_skills = get_basic_skills() + get_advanced_skills()
    return all_skills


def get_basic_skills():
    basic_skills = [skill.value for skill in BasicSkills]
    return basic_skills


def get_advanced_skills():
    advanced_skills = [skill.value for skill in AdvancedSkills]
    return advanced_skills


class BasicSkills(Enum):
    AWARENESS = 'awareness'
    CAROUSE = 'carouse'
    CHARM = 'charm'
    CLIMB = 'climb'
    COMMAND = 'command'
    CONCEALMENT = 'concealment'
    CONTORTIONIST = 'contortionist'
    DECEIVE = 'deceive'
    DODGE = 'dodge'
    EVALUATE = 'evaluate'
    GAMBLE = 'gamble'
    INQUIRY = 'inquiry'
    INTIMIDATE = 'intimidate'
    LOGIC = 'logic'
    SCRUTINY = 'scrutiny'
    SEARCH = 'search'
    SILENT_MOVE = 'silent_move'
    SWIM = 'swim'


class AdvancedSkills(Enum):
    ACROBATICS = 'acrobatics'
    CHEM_USE = 'chem_use'
    CIPHERS = 'ciphers'
    DEMOLITION = 'demolition'
    DRIVE = 'drive'
    INTERROGATION = 'interrogation'
    INVOCATION = 'invocation'
    LIP_READING = 'lip_reading'
    LITERACY = 'literacy'
    LORE_COMMON = 'lore_common'
    LORE_FORBIDDEN = 'lore_forbidden'
    LORE_SCHOLASTIC = 'lore_scholastic'
    MEDICAE = 'medicae'
    NAVIGATION = 'navigation'
    PERFORMER = 'performer'
    PILOT = 'pilot'
    PSYNISCIENCE = 'psyniscience'
    SECURITY = 'security'
    SHADOWING = 'shadowing'
    SLEIGHT_OF_HAND = 'sleight_of_hand'
    SPEAK_LANGUAGE = 'speak_language'
    SURVIVAL = 'survival'
    TACTICS = 'tactics'
    TECH_USE = 'tech_use'
    TRACKING = 'tracking'
    TRADE = 'trade'
    WRANGLING = 'wrangling'


def get_skill_characteristic(active_skill):
    for char_stat, skills in get_skill_characteristic_mappings().iteritems():
        for skill in skills:
            if active_skill.lower() == skill.value:
                return char_stat
    return None


def get_skill_characteristic_mappings():
    return {STAT_STR: (BasicSkills.CLIMB,
                       BasicSkills.INTIMIDATE,
                       BasicSkills.SWIM),
            STAT_PER: (BasicSkills.AWARENESS,
                       BasicSkills.GAMBLE,
                       BasicSkills.SEARCH,
                       BasicSkills.SCRUTINY,
                       AdvancedSkills.LIP_READING,
                       AdvancedSkills.PSYNISCIENCE),
            STAT_TGH: (BasicSkills.CAROUSE,),
            STAT_FEL: (BasicSkills.CHARM,
                       BasicSkills.COMMAND,
                       BasicSkills.DECEIVE,
                       BasicSkills.INQUIRY,
                       AdvancedSkills.PERFORMER),
            STAT_AGI: (BasicSkills.CONCEALMENT,
                       BasicSkills.CONTORTIONIST,
                       BasicSkills.DODGE,
                       BasicSkills.SILENT_MOVE,
                       AdvancedSkills.ACROBATICS,
                       AdvancedSkills.DRIVE,
                       AdvancedSkills.PILOT,
                       AdvancedSkills.SECURITY,
                       AdvancedSkills.SHADOWING,
                       AdvancedSkills.SLEIGHT_OF_HAND),
            STAT_WIL: (AdvancedSkills.INTERROGATION,
                       AdvancedSkills.INVOCATION),
            STAT_INT: (BasicSkills.EVALUATE,
                       BasicSkills.LOGIC,
                       AdvancedSkills.CHEM_USE,
                       AdvancedSkills.CIPHERS,
                       AdvancedSkills.DEMOLITION,
                       AdvancedSkills.LITERACY,
                       AdvancedSkills.LORE_COMMON,
                       AdvancedSkills.LORE_FORBIDDEN,
                       AdvancedSkills.LORE_SCHOLASTIC,
                       AdvancedSkills.MEDICAE,
                       AdvancedSkills.NAVIGATION,
                       AdvancedSkills.SPEAK_LANGUAGE,
                       AdvancedSkills.SURVIVAL,
                       AdvancedSkills.TACTICS,
                       AdvancedSkills.TECH_USE,
                       AdvancedSkills.TRACKING,
                       AdvancedSkills.TRADE,
                       AdvancedSkills.WRANGLING)}
