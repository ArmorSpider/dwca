from copy import deepcopy
import json

from definitions import ATTACKER, TARGET, WEAPON, FIREMODE, NUM_ATTACKS,\
    ROLL_TARGET, ATTACKER_MAG, TARGET_MAG, RUN, QUIT, CLEAR, AUTO, AIMED, CHARGE,\
    OVERLOADED, COVER, DAMAGE, SAVE, LOAD
from src.action.attack import Attack
from src.action.hit import Hit
from src.cli.commands import process_command
from src.cli.match_map import get_default_match_map
from src.cli.message_queue import log_messages
from src.dwca_log.log import get_log
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.char_stats import STAT_WS, STAT_BS
from src.entities.libraries import get_character_library, get_weapon_library,\
    find_best_match
from src.entities.weapon import get_weapon
from src.errors import NoMatchError
from src.handler import check_required_keys, build_attacker, main_handler,\
    build_target
from src.hit_location import BODY
from src.modifiers.modifier import register_modifiers
from src.situational.state_manager import StateManager
from src.util.dict_util import pretty_print
from src.util.string_util import normalize_string
from src.util.user_input import user_choose_from_list, user_input_int


LOG = get_log(__name__)

SAVED_STATES = {}


def cli_loop_2():
    event = {}
    while True:
        cleanup_event(event)
        display_event(event)
        command_string = raw_input('Enter commands: \n')
        try:
            event = process_command(command_string, event)
        except (ValueError, NoMatchError) as error:
            LOG.error(error.message)


def save_state(event):
    state_name = raw_input('Save state as: ')
    clean_state_name = normalize_string(state_name)
    try:
        SAVED_STATES[clean_state_name] = deepcopy(event)
    except Exception:
        print 'Save state failed.'
    else:
        print 'Saved state as "%s"' % state_name


def load_state():
    available_states = SAVED_STATES.keys()
    print 'Available states:'
    pretty_print(available_states)
    state_name = raw_input('Load which state? ')
    state_name_best_match = find_best_match(state_name, available_states)
    state = deepcopy(SAVED_STATES[state_name_best_match])
    return state


def display_event(event):
    print '[CURRENT EVENT]'
    print json.dumps(event, indent=4)


def cleanup_event(event):
    for key, value in event.items():
        if not value:
            event.pop(key)


def main():
    cli_loop_2()


if __name__ == '__main__':
    main()
