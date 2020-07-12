from definitions import ATTACKER, TARGET, WEAPON, FIREMODE, NUM_ATTACKS,\
    ROLL_TARGET, ATTACKER_MAG, TARGET_MAG, OVERLOADED,\
    ROLL_RESULT, ROLL_MODIFIERS, RANGE, DEBUG
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.libraries import get_character_library, get_weapon_library


def get_default_match_map():
    match_map = {ATTACKER: list(get_character_library().keys()),
                 TARGET: list(get_character_library().keys()),
                 WEAPON: list(get_weapon_library().keys()),
                 FIREMODE: [SINGLE_SHOT, SEMI_AUTO, FULL_AUTO],
                 ROLL_MODIFIERS: None,
                 ROLL_RESULT: None,
                 NUM_ATTACKS: None,
                 ROLL_TARGET: None,
                 ATTACKER_MAG: None,
                 TARGET_MAG: None,
                 OVERLOADED: None,
                 RANGE: None,
                 DEBUG: None}
    return match_map
