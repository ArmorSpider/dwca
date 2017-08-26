import re

from src.cli import build_attack_event
from src.dwca_log.log import get_log
from src.entities.character import get_char
from src.entities.horde import get_horde
from src.entities.weapon import get_weapon
from src.message_queue import log_messages
from src.modifiers.modifier import register_modifiers
from src.util.string_util import convert_to_snake_case


LOG = get_log(__name__)


def main():
    event = build_attack_event()
    register_modifiers()
    main_handler(event)
    log_messages()


def main_handler(event):
    attack_damages = multiple_attacks(event)
    total_damage = sum(attack_damages)
    LOG.info('Total damage: %s (%s)', total_damage,
             ' + '.join([str(attack_damage) for attack_damage in attack_damages]))


def construct_attack(event):
    attacker = construct_attacker(event)
    target = construct_target(event)
    weapon = construct_weapon(event)
    firemode = event.get('firemode')
    attack = attacker.attack(weapon, target, firemode)
    roll_target = event['roll_target']
    attack.try_action(roll_target=roll_target,
                      roll_result=None)
    return attack


def construct_weapon(event):
    weapon_string = event['weapon']
    weapon_name = convert_to_snake_case(weapon_string)
    weapon = get_weapon(weapon_name)
    return weapon


def construct_entity(entity_string):
    match = re.search(r'\s\d+$', entity_string)
    if match is not None:
        match_string = match.group()
        magnitude = int(match_string.lstrip())
        attacker_name = entity_string.split(match_string)[0]
    else:
        magnitude = None
        attacker_name = entity_string

    attacker_name = convert_to_snake_case(attacker_name)
    if magnitude is not None:
        attacker = get_horde(creature_name=attacker_name,
                             magnitude=magnitude)
    else:
        attacker = get_char(char_name=attacker_name)
    return attacker


def construct_attacker(event):
    attacker_string = event['attacker']
    return construct_entity(entity_string=attacker_string)


def construct_target(event):
    target_string = event['target']
    return construct_entity(entity_string=target_string)


def try_attack(event):
    LOG.info('__________NEW ATTACK__________')
    attack = construct_attack(event)
    attack_damage = attack.apply_hits()
    return attack_damage


def multiple_attacks(event):
    num_attacks = event.get('num_attacks', 1)
    attack_damages = []
    for _ in range(num_attacks):
        attack_damage = try_attack(event)
        attack_damages.append(attack_damage)
    return attack_damages


if __name__ == '__main__':
    main()
