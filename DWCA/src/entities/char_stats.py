from enum import Enum


class CharStat(Enum):
    WEAPON_SKILL = 'weapon skill'
    BALLISTIC_SKILL = 'ballistic skill'
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
