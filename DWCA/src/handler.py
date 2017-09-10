from definitions import FIREMODE, ROLL_TARGET, WEAPON, ATTACKER, ATTACKER_MAG,\
    TARGET, TARGET_MAG, NUM_ATTACKS
from src.dwca_log.log import get_log
from src.entities.character import get_char
from src.entities.horde import get_horde
from src.entities.weapon import get_weapon


LOG = get_log(__name__)


def main_handler(event):
    attack_damages = multiple_attacks(event)
    total_damage = sum(attack_damages)
    LOG.info('All attacks combined damage: %s (%s)', total_damage,
             ' + '.join([str(attack_damage) for attack_damage in attack_damages]))


def check_required_keys(event, required_keys):
    missing_keys = []
    for key in required_keys:
        if key not in event:
            missing_keys.append(key)
    if missing_keys != []:
        raise ValueError('Missing keys: %s' % missing_keys)


def construct_attack(event):
    attacker = build_attacker(event)
    target = build_target(event)
    weapon = build_weapon(event)
    firemode = event.get(FIREMODE)
    attack = attacker.attack(weapon, target, firemode)
    roll_target = event[ROLL_TARGET]
    attack.try_action(roll_target=roll_target,
                      roll_result=None)
    return attack


def build_weapon(event):
    weapon_name = event[WEAPON]
    weapon = get_weapon(weapon_name)
    return weapon


def build_attacker(event):
    char_name = event[ATTACKER]
    magnitude = event.get(ATTACKER_MAG)
    if magnitude is None:
        return get_char(char_name)
    else:
        return get_horde(char_name, magnitude)


def build_target(event):
    char_name = event[TARGET]
    magnitude = event.get(TARGET_MAG)
    if magnitude is None:
        return get_char(char_name)
    else:
        return get_horde(char_name, magnitude)


def single_attack(event, attack_number):
    LOG.info('________[ATTACK %s]________', attack_number)
    attack = construct_attack(event)
    attack_damage = attack.apply_hits()
    return attack_damage


def multiple_attacks(event):
    num_attacks = event.get(NUM_ATTACKS, 1)
    attack_damages = []
    for attack_number in range(int(num_attacks)):
        attack_damage = single_attack(event, attack_number + 1)
        attack_damages.append(attack_damage)
    return attack_damages
