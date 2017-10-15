import sys

from definitions import FIREMODE, WEAPON, NUM_ATTACKS, ROLL_TARGET, ATTACKER,\
    TARGET, OVERLOADED, CHARGE, AIMED, COVER
from src.action.attack import Attack
from src.action.hit import Hit
from src.cli.match_map import get_default_match_map
from src.cli.message_queue import log_messages
from src.cli.quick_dict import quick_dict_parse
from src.dwca_log.log import get_log
from src.entities import SEMI_AUTO, FULL_AUTO
from src.entities.char_stats import STAT_WS, STAT_BS
from src.entities.libraries import get_weapon_library, get_character_library
from src.entities.weapon import get_weapon
from src.handler import build_attacker, main_handler, check_required_keys,\
    build_target
from src.hit_location import BODY
from src.modifiers.modifier import register_modifiers
from src.save_manager import SaveManager
from src.situational.state_manager import StateManager
from src.util.dict_util import pretty_print
from src.util.string_util import normalize_string
from src.util.user_input import user_choose_from_list, user_input_int


LOG = get_log(__name__)


def process_command(command_string, event):
    for command in known_commands_generator():
        if command.is_this_command(command_string):
            event = command.process_command(event)
            break
    else:
        quick_dict = quick_dict_parse(command_string, get_default_match_map())
        event.update(quick_dict)
    return event


def known_commands_generator():
    commands = [cls() for cls in CLICommand.__subclasses__()]
    for command in commands:
        yield command


class CLICommand(object):

    keyword = None
    required_keys = []

    def is_this_command(self, command_string):
        normalized_string = normalize_string(command_string)
        return normalized_string == self.keyword

    def process_command(self, event):
        check_required_keys(event, self.required_keys)
        updated_event = self._process_event(event)
        return updated_event

    def _process_event(self, event):
        return event

    def _toggle_key(self, key, event):
        if key in event:
            event.pop(key)
        else:
            event[key] = True
        return event


class CommandRun(CLICommand):

    keyword = 'run'
    required_keys = [ATTACKER, TARGET, WEAPON, ROLL_TARGET]

    def _process_event(self, event):
        register_modifiers()
        StateManager.update(event)
        main_handler(event)
        log_messages()
        return event


class CommandQuit(CLICommand):

    keyword = 'quit'

    def _process_event(self, event):
        sys.exit(0)


class CommandWeapon(CLICommand):

    keyword = 'weapon'

    def _process_event(self, event):
        weapon_name = user_choose_from_list(get_weapon_library().keys())
        event[WEAPON] = weapon_name
        return event


class CommandAttacker(CLICommand):

    keyword = 'attacker'

    def _process_event(self, event):
        character_name = user_choose_from_list(get_character_library().keys())
        event[ATTACKER] = character_name
        return event


class CommandTarget(CLICommand):

    keyword = 'target'

    def _process_event(self, event):
        character_name = user_choose_from_list(get_character_library().keys())
        event[TARGET] = character_name
        return event


class CommandOverload(CLICommand):

    keyword = 'overload'

    def _process_event(self, event):
        event = self._toggle_key(OVERLOADED, event)
        return event


class CommandCover(CLICommand):

    keyword = 'cover'

    def _process_event(self, event):
        armor_value = user_input_int('Enter cover armor value: ')
        if armor_value:
            event[COVER] = armor_value
        else:
            event.pop(COVER, None)
        return event


class CommandCharge(CLICommand):

    keyword = 'charge'

    def _process_event(self, event):
        event = self._toggle_key(CHARGE, event)
        return event


class CommandAim(CLICommand):

    keyword = 'aim'

    def _process_event(self, event):
        event = self._toggle_key(AIMED, event)
        return event


class CommandSave(CLICommand):

    keyword = 'save'

    def _process_event(self, event):
        state_name = raw_input('Save state as: ')
        clean_state_name = normalize_string(state_name)
        SaveManager.save_state(clean_state_name, event)
        return event


class CommandLoad(CLICommand):

    keyword = 'load'

    def _process_event(self, event):
        available_states = SaveManager.saved_states.keys()
        LOG.info('Available states:')
        pretty_print(available_states)
        state_name = raw_input('Load which state? ')
        clean_state_name = normalize_string(state_name)
        state = SaveManager.load_state(clean_state_name)
        return state


class CommandDamage(CLICommand):

    keyword = 'damage'
    required_keys = [ATTACKER, TARGET]

    def _process_event(self, event):
        damage = 0
        hits = []
        penetration = user_input_int('Enter penetration: ')

        while damage != 'done':
            damage = raw_input('Enter damage: ')
            if damage == 'done':
                continue
            hit = Hit(BODY, damage, penetration)
            hits.append(hit)
        register_modifiers()
        StateManager.update(event)
        target = build_target(event)
        attacker = build_attacker(event)
        dummy_weapon = get_weapon('dummy')
        attack = Attack(weapon=dummy_weapon,
                        attacker=attacker,
                        target=target)
        attack.apply_hits(custom_hits=hits)
        return event


class CommandAuto(CLICommand):

    keyword = 'auto'
    required_keys = [ATTACKER]

    def _process_event(self, event):
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
            if weapon.get_quality('twin_linked', False):
                LOG.info('+20 to roll target from twin-linked.')
                roll_target += 20
            event[FIREMODE] = firemode
        event[WEAPON] = weapon_name
        event[NUM_ATTACKS] = num_attacks
        event[ROLL_TARGET] = roll_target
        return event


class CommandClear(CLICommand):

    keyword = 'clear'

    def _process_event(self, event):
        event.clear()
        return event
