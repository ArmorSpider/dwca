import sys

from definitions import WEAPON, ROLL_TARGET, ATTACKER,\
    TARGET, OVERLOADED, CHARGED, AIMED, COVER, AD_HOC, ROLL_RESULT, RANGE
from src.action.hit import Hit
from src.cli.auto_module import auto_assemble, range_module, equip_weapon
from src.cli.info_module import info_module
from src.cli.match_map import get_default_match_map
from src.cli.message_queue import log_messages
from src.cli.new_module import new_module
from src.cli.quick_dict import quick_dict_parse
from src.cli.run_module import run_module
from src.cli.table import print_table
from src.dwca_log.log import get_log
from src.entities.libraries import get_weapon_library, get_character_library,\
    MasterLibrary
from src.handler import check_required_keys,\
    build_attack, build_attacker, build_weapon
from src.hitloc_series import build_hitloc_iterator
from src.modifiers.roll_modifier import CHARGE_MOD, AIM_MOD, add_roll_mod
from src.save_manager import SaveManager
from src.situational.state_manager import StateManager
from src.util.dict_util import pretty_print
from src.util.event_util import update_adhoc_dict
from src.util.string_util import normalize_string
from src.util.user_input import try_user_choose_from_list, user_input_int


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
    commands = [cls()
                for cls in CLICommand.__subclasses__()]  # pylint: disable=E1101
    for command in commands:
        yield command


class CLICommand(object):

    keyword = None
    required_keys = []
    help = 'Does stuff'

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

    def _toggle_adhoc_key(self, key, event, value=True):
        ad_hoc = event.get(AD_HOC, {})
        if key in ad_hoc:
            ad_hoc.pop(key)
        else:
            ad_hoc[key] = value
        event[AD_HOC] = ad_hoc
        return event


class CommandHelp(CLICommand):

    keyword = 'help'
    help = 'Shows available commands.'

    def _process_event(self, event):
        table_data = []
        for command in known_commands_generator():
            row = [command.keyword, command.help]
            table_data.append(row)
        print_table(table_data, title='Available commands', headers=False)
        return event


class CommandBonus(CLICommand):

    keyword = 'bonus'
    help = 'Add a to-hit bonus'

    def _process_event(self, event):
        bonus_value = user_input_int('Enter bonus: ')
        event = add_roll_mod(event, bonus_value)
        return event


class CommandMalus(CLICommand):

    keyword = 'malus'
    help = 'Add a to-hit malus'

    def _process_event(self, event):
        malus_value = -user_input_int('Enter malus: ')
        event = add_roll_mod(event, malus_value)
        return event


class ComandAdHoc(CLICommand):

    keyword = 'adhoc'
    help = 'Manually add temporary modifiers.'

    def _process_event(self, event):
        input_string = raw_input('Enter ad-hoc dict string: ')
        ad_hoc_dict = quick_dict_parse(input_string)
        event = update_adhoc_dict(event, ad_hoc_dict)
        return event


class CommandRun(CLICommand):

    keyword = 'run'
    required_keys = [ATTACKER, TARGET, WEAPON, ROLL_TARGET]
    help = 'Roll attacks for the current event.'

    def _process_event(self, event):
        event = run_module(event)
        return event


class CommandReload(CLICommand):

    keyword = 'reload'
    help = 'Reload character & weapon libraries.'

    def _process_event(self, event):
        MasterLibrary.reload_libraries(self)
        return event


class CommandInfo(CLICommand):

    keyword = 'info'
    required_keys = []
    help = 'Show talents & traits for character.'

    def _process_event(self, event):
        event = info_module(event)
        return event


class CommandQuit(CLICommand):

    keyword = 'quit'
    help = 'Terminate this program.'

    def _process_event(self, event):
        sys.exit(0)


class CommandPackage(CLICommand):

    keyword = 'package'
    help = 'Load a package of weapons and characters.'

    def _process_event(self, event):
        LOG.info('Choose package to load:')
        known_packages = MasterLibrary.get_known_packages()
        loaded_packages = MasterLibrary.get_loaded_packages()
        non_loaded_packages = [
            package for package in known_packages if package not in loaded_packages]
        package_name = try_user_choose_from_list(non_loaded_packages)
        MasterLibrary.add_package(package_name)
        return event


class CommandEquip(CLICommand):

    keyword = 'equip'
    help = 'Choose weapon from a list of available weapons.'

    def _process_event(self, event):
        weapon_name = try_user_choose_from_list(get_weapon_library().keys())
        event[WEAPON] = weapon_name
        event = equip_weapon(event)
        return event


class CommandNew(CLICommand):

    keyword = 'new'
    help = 'Configure new attack.'

    def _process_event(self, event):
        event = new_module(event)
        return event


class CommandAttacker(CLICommand):

    keyword = 'attacker'
    help = 'Choose attacker from a list of available characters.'

    def _process_event(self, event):
        character_name = try_user_choose_from_list(
            get_character_library().keys())
        event[ATTACKER] = character_name
        return event


class CommandTarget(CLICommand):

    keyword = 'target'
    help = 'Choose target from a list of available characters.'

    def _process_event(self, event):
        character_name = try_user_choose_from_list(
            get_character_library().keys())
        event[TARGET] = character_name
        return event


class CommandOverload(CLICommand):

    keyword = 'overload'
    help = 'Toggle overload TRUE/FALSE for current event.'

    def _process_event(self, event):
        event = self._toggle_key(OVERLOADED, event)
        return event


class CommandRange(CLICommand):

    keyword = 'range'
    help = 'Set range to target and update hit modifiers.'
    required_keys = [WEAPON]

    def _process_event(self, event):
        range_ = user_input_int('Enter range to target: ')
        event[RANGE] = range_
        event = range_module(event)
        return event


class CommandCover(CLICommand):

    keyword = 'cover'
    help = 'Add cover to the current event.'

    def _process_event(self, event):
        armor_value = user_input_int('Enter cover armor value: ')
        event = self._toggle_adhoc_key(COVER, event, armor_value)
        return event


class CommandCharge(CLICommand):

    keyword = 'charge'
    help = 'Toggle charge TRUE/FALSE for current event.'

    def _process_event(self, event):
        event = self._toggle_adhoc_key(CHARGED, event)
        attacker = build_attacker(event)
        charge_bonus = 10
        if attacker.berserk_charge is not None:
            LOG.debug('+20 when charging from BerserkCharge.')
            charge_bonus = 20
        event = add_roll_mod(event, charge_bonus, CHARGE_MOD)
        return event


class CommandAim(CLICommand):

    keyword = 'aim'
    help = 'Toggle aim TRUE/FALSE for the current event'

    def _process_event(self, event):
        event = self._toggle_adhoc_key(AIMED, event)
        weapon = build_weapon(event)
        aim_bonus = 10
        if weapon.accurate is not None:
            LOG.debug('Additional +10 when aiming from Accurate.')
            aim_bonus += 10
        event = add_roll_mod(event, aim_bonus, AIM_MOD)
        return event


class CommandSave(CLICommand):

    keyword = 'save'
    help = 'Save the current event for this session.'

    def _process_event(self, event):
        state_name = raw_input('Save state as: ')
        clean_state_name = normalize_string(state_name)
        SaveManager.save_state(clean_state_name, event)
        return event


class CommandLoad(CLICommand):

    keyword = 'load'
    help = 'Load a saved event.'

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
    help = 'Manually enter the total damage of hits and calculate effective damage.'
    required_keys = [ATTACKER, TARGET, WEAPON]

    def _process_event(self, event):
        damage = 0
        hits = []
        penetration = user_input_int('Enter penetration: ')
        roll_result = user_input_int('Enter roll result: ')
        event[ROLL_RESULT] = roll_result
        attack = build_attack(event)
        hitloc_iterator = build_hitloc_iterator(attack.hit_location)

        while damage != 'done':
            damage = raw_input('Enter damage: ')
            if damage == 'done':
                continue
            hit = Hit(hitloc_iterator.next(), damage, penetration)
            hits.append(hit)
        StateManager.update(event)
        attack.apply_hits(hits=hits)
        log_messages()
        return event


class CommandAuto(CLICommand):

    keyword = 'auto'
    help = 'Auto configure event based on attacker.'
    required_keys = [ATTACKER]

    def _process_event(self, event):
        event = auto_assemble(event)
        return event


class CommandClear(CLICommand):

    keyword = 'clear'
    help = 'Clear the current event.'

    def _process_event(self, event):
        event.clear()
        return event
