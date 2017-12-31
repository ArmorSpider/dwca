from definitions import FIREMODE, ROLL_TARGET, WEAPON, ATTACKER, ATTACKER_MAG,\
    TARGET, TARGET_MAG, NUM_ATTACKS, AD_HOC, ROLL_RESULT
from src.dwca_log.log import get_log
from src.entities.entity_factory import build_entity
from src.entities.weapon import get_weapon
from src.modifiers.roll_modifier import get_effective_modifier
from src.util.dict_util import pretty_print


LOG = get_log(__name__)


def main_handler(event):
    attack_damages = multiple_attacks(event)
    num_damages = len(attack_damages)
    raw_damage = sum(attack_damages)
    dps = raw_damage / num_damages
    LOG.info('All attacks combined damage: %s (%s)', raw_damage,
             ' + '.join([str(attack_damage) for attack_damage in attack_damages]))
    LOG.info('DPS: %s', dps)


def check_required_keys(event, required_keys):
    missing_keys = []
    for key in required_keys:
        if key not in event:
            missing_keys.append(key)
    if missing_keys != []:
        raise ValueError('Missing keys: %s' % missing_keys)


def build_attack(event):
    attacker = build_attacker(event)
    target = build_target(event)
    weapon = build_weapon(event)
    firemode = event.get(FIREMODE)
    ad_hoc_modifiers = event.get(AD_HOC, {})
    attack = attacker.attack(weapon, target, firemode)
    attack.ad_hoc_modifiers = ad_hoc_modifiers
    roll_target = event.get(ROLL_TARGET, 0)
    roll_target += get_effective_modifier(event)
    roll_result = event.get(ROLL_RESULT, None)
    attack.try_action(roll_target=roll_target,
                      roll_result=roll_result)
    return attack


def build_weapon(event):
    weapon_name = event[WEAPON]
    weapon = get_weapon(weapon_name)
    return weapon


def build_attacker(event):
    char_name = event[ATTACKER]
    magnitude = event.get(ATTACKER_MAG)
    attacker = build_entity(char_name, magnitude)
    return attacker


def build_target(event):
    char_name = event[TARGET]
    magnitude = event.get(TARGET_MAG)
    target = build_entity(char_name, magnitude)
    return target


def single_attack(event, attack_number):
    LOG.info('________[ATTACK %s]________', attack_number)
    attack = build_attack(event)
    attack_damage = attack.apply_attack()
    if event.get('debug') is not None:
        pretty_print(attack.metadata)
    return attack_damage


def multiple_attacks(event):
    num_attacks = event.get(NUM_ATTACKS, 1)
    attack_damages = []
    for attack_number in range(int(num_attacks)):
        attack_damage = single_attack(event, attack_number + 1)
        attack_damages.append(attack_damage)
    return attack_damages
