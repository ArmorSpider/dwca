import json

from definitions import ATTACKER, TARGET, WEAPON, FIREMODE, NUM_ATTACKS,\
    ROLL_TARGET, ATTACKER_MAG, TARGET_MAG, RUN, QUIT, CLEAR, AUTO, AIMED, CHARGE,\
    OVERLOADED
from src.dwca_log.log import get_log
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.char_stats import STAT_WS, STAT_BS
from src.entities.weapon import get_weapon
from src.handler import check_required_keys, build_attacker, main_handler
from src.message_queue import log_messages
from src.modifiers.modifier import register_modifiers
from src.state_manager import StateManager
from src.util.read_file import find_best_match, get_character_library,\
    get_weapon_library
from src.util.user_input import user_choose_from_list


LOG = get_log(__name__)


EVENT_BASE = {ATTACKER: get_character_library().keys(),
              TARGET: get_character_library().keys(),
              WEAPON: get_weapon_library().keys(),
              FIREMODE: [SINGLE_SHOT, SEMI_AUTO, FULL_AUTO],
              NUM_ATTACKS: None,
              ROLL_TARGET: None,
              ATTACKER_MAG: None,
              TARGET_MAG: None,
              AIMED: None,
              CHARGE: None,
              OVERLOADED: None}


def cli_loop():
    user_input = None
    event = {}
    while user_input != QUIT:
        cleanup_event(event)
        display_event(event)
        try:
            user_input = raw_input('Enter commands: \n').lower()
            handle_user_input(user_input, event)
        except Exception:
            LOG.exception('Something went wrong.')


def handle_user_input(user_input, event):
    if ':' in user_input:
        update_dict = parse_event_update_string(user_input)
        event.update(update_dict)
    if user_input == RUN:
        check_required_keys(
            event, [ATTACKER, TARGET, WEAPON, ROLL_TARGET])
        run_event(event)
    if user_input == CLEAR:
        event = {}
    if user_input == AUTO:
        check_required_keys(event, [ATTACKER])
        event = auto_module(event)


def display_event(event):
    print '[CURRENT EVENT]'
    print json.dumps(event, indent=4)


def cleanup_event(event):
    for key, value in event.items():
        if not value:
            event.pop(key)


def auto_module(event):
    attacker = build_attacker(event)
    weapon_name = user_choose_from_list(attacker.weapons)
    weapon = get_weapon(weapon_name)
    if weapon.is_melee():
        num_attacks = attacker.get_num_melee_attacks()
        roll_target = attacker.get_characteristic(STAT_WS)
    else:
        num_attacks = attacker.get_num_ranged_attacks()
        roll_target = attacker.get_characteristic(STAT_BS)
        firemodes = weapon.firemodes.keys()
        firemode = user_choose_from_list(firemodes)
        if firemode == SEMI_AUTO:
            LOG.info('+10 to roll target from semi auto.')
            roll_target += 10
        elif firemode == FULL_AUTO:
            LOG.info('+20 to roll target from full auto.')
            roll_target += 20
        event[FIREMODE] = firemode
    event[WEAPON] = weapon_name
    event[NUM_ATTACKS] = num_attacks
    event[ROLL_TARGET] = roll_target
    return event


def parse_event_update_string(key_value_string):
    event_update_dict = {}
    for key_value_pair in key_value_string.split(','):
        key, value = parse_key_value_pair(key_value_pair)
        best_match_key = find_best_match(key, EVENT_BASE.keys())
        print best_match_key
        if best_match_key is None:
            LOG.info('No match for "%s".', key)
            continue
        matches = EVENT_BASE.get(best_match_key)
        if matches is not None:
            best_match_value = find_best_match(value, matches)
        else:
            best_match_value = value
        if best_match_value is not None:
            event_update_dict[best_match_key] = best_match_value
        else:
            LOG.info('No match for "%s".', value)
            continue
    return event_update_dict


def parse_key_value_pair(key_value_pair):
    split_thing = key_value_pair.split(':')
    key = split_thing[0].strip()
    value = split_thing[-1].strip()
    return key, value


def run_event(event):
    register_modifiers()
    StateManager.update(event)
    main_handler(event)
    log_messages()


def main():
    cli_loop()


if __name__ == '__main__':
    main()
