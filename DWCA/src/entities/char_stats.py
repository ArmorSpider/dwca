from enum import Enum


class CharStat(Enum):
    WEAPON_SKILL = 'weapon_skill'
    BALLISTIC_SKILL = 'ballistic_skill'
    STRENGTH = 'strength'
    TOUGHNESS = 'toughness'
    AGILITY = 'agility'
    INTELLIGENCE = 'intelligence'
    PERCEPTION = 'perception'
    WILLPOWER = 'willpower'
    FELLOWSHIP = 'fellowship'


STAT_WS = CharStat.WEAPON_SKILL.value
STAT_BS = CharStat.BALLISTIC_SKILL.value
STAT_STR = CharStat.STRENGTH.value
STAT_TGH = CharStat.TOUGHNESS.value
STAT_AGI = CharStat.AGILITY.value
STAT_INT = CharStat.INTELLIGENCE.value
STAT_PER = CharStat.PERCEPTION.value
STAT_WIL = CharStat.WILLPOWER.value
STAT_FEL = CharStat.FELLOWSHIP.value

ALL_CHARACTERISTICS = [STAT_WS,
                       STAT_BS,
                       STAT_STR,
                       STAT_TGH,
                       STAT_AGI,
                       STAT_INT,
                       STAT_PER,
                       STAT_WIL,
                       STAT_FEL]
