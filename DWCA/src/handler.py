from definitions import FIREMODE, ROLL_TARGET, WEAPON, ATTACKER, ATTACKER_MAG,\
    TARGET, TARGET_MAG, AD_HOC, ROLL_RESULT
from src.dwca_log.log import get_log
from src.entities import DUMMY
from src.entities.character import choose_character
from src.entities.entity_factory import build_entity
from src.entities.weapon import get_weapon
from src.modifiers.roll_modifier import get_effective_modifier


LOG = get_log(__name__)


def check_required_keys(event, required_keys):
    missing_keys = []
    for key in required_keys:
        if key not in event:
            missing_keys.append(key)
    if missing_keys != []:
        raise ValueError('Missing keys: %s' % missing_keys)


def choose_or_build_attacker(event):
    if ATTACKER not in event:
        event[ATTACKER] = choose_character()
    character = build_attacker(event)
    return character


def build_attack(event):
    attack = build_base_attack(event)
    roll_target = event.get(ROLL_TARGET, 0)
    roll_target += get_effective_modifier(event)
    roll_result = event.get(ROLL_RESULT, None)
    attack.try_action(roll_target=roll_target,
                      roll_result=roll_result)
    return attack


def build_base_attack(event):
    attacker = build_attacker(event)
    target = build_target(event)
    weapon = build_weapon(event)
    firemode = event.get(FIREMODE)
    ad_hoc_modifiers = event.get(AD_HOC, {})
    attack = attacker.attack(weapon, target, firemode)
    attack.ad_hoc_modifiers = ad_hoc_modifiers
    return attack


def build_weapon(event):
    weapon_name = event.get(WEAPON, DUMMY)
    weapon = get_weapon(weapon_name)
    return weapon


def build_attacker(event):
    char_name = event[ATTACKER]
    magnitude = event.get(ATTACKER_MAG)
    attacker = build_entity(char_name, magnitude)
    return attacker


def build_target(event):
    char_name = event.get(TARGET, DUMMY)
    magnitude = event.get(TARGET_MAG)
    target = build_entity(char_name, magnitude)
    return target
