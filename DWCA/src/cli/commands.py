from copy import deepcopy
import sys

from definitions import WEAPON, ROLL_TARGET, ATTACKER,\
    TARGET, OVERLOADED, CHARGED, AIMED, COVER, AD_HOC, ROLL_RESULT, RANGE,\
    HELPLESS, TARGET_MAG, ATTACKER_MAG
from src.action.action import try_action
from src.action.hit import Hit
from src.cli.match_map import get_default_match_map
from src.cli.message_queue import log_messages
from src.cli.quick_dict import quick_dict_parse
from src.cli.read_metadata import present_metadata
from src.cli.table import print_table
from src.dwca_log.log import get_log
from src.entities import HALF_MOVE, FULL_MOVE, CHARGE_MOVE, RUN_MOVE
from src.entities.libraries import get_weapon_library, get_character_library,\
    MasterLibrary, find_best_match
from src.handler import check_required_keys,\
    build_attacker, build_weapon, build_base_attack, choose_or_build_attacker,\
    build_attack
from src.hitloc_series import build_hitloc_iterator
from src.modifiers.roll_modifier import CHARGE_MOD, AIM_MOD, add_roll_mod,\
    get_effective_modifier
from src.modules.auto_module import handler_auto
from src.modules.dps_module import handler_dps
from src.modules.equip_module import handler_equip
from src.modules.info_module import handler_info
from src.modules.new_module import handler_new
from src.modules.profile_module import handler_profile
from src.modules.range_module import handler_range
from src.modules.raw_module import handler_rawdef
from src.modules.reaction_module import handler_defend
from src.modules.run_module import handler_run
from src.save_manager import SaveManager
from src.situational.scatter import scatter
from src.situational.state_manager import StateManager
from src.util.dict_util import pretty_print
from src.util.event_util import update_adhoc_dict
from src.util.string_util import normalize_string
from src.util.user_input import try_user_choose_from_list, user_input_int,\
    user_input_string, try_user_input_int


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
    args = []

    def is_this_command(self, command_string):
        split_command = command_string.split(' ', 1)
        match = normalize_string(split_command[0]) == self.keyword
        del split_command[0]
        self.args = split_command
        return match

    def process_command(self, event):
        LOG.info('Running command "%s" with args %s', self.keyword, self.args)
        check_required_keys(event, self.required_keys)
        updated_event = self._process_event(event)
        return updated_event

    def _process_event(self, event):
        return event

    def smart_select_attacker(self, event):
        attacker = self.get_arg_or_select_from_list(
            'Select character: ', get_character_library().keys())
        event_copy = deepcopy(event)
        event_copy[ATTACKER] = attacker
        return event_copy

    def smart_select_target(self, event):
        target = self.get_arg_or_select_from_list(
            'Select character: ', get_character_library().keys())
        event_copy = deepcopy(event)
        event_copy[TARGET] = target
        return event_copy

    def get_arg_or_input_int(self, prompt):
        try:
            value = int(self.args[0])
        except IndexError:
            value = user_input_int(prompt)
        return value

    def get_arg_or_input_string(self, prompt):
        try:
            value = str(self.args[0])
        except IndexError:
            value = user_input_string(prompt)
        return value

    def get_arg_or_select_from_list(self, prompt, options):
        try:
            raw_value = self.args[0]
            value = find_best_match(raw_value, options)
        except IndexError:
            LOG.info(prompt)
            value = try_user_choose_from_list(options)
        return value

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


class CommandDPS(CLICommand):

    keyword = 'dps'
    help = 'Calculate DPS metrics for event'
    required_keys = [ATTACKER, WEAPON, TARGET]

    def _process_event(self, event):
        event = handler_dps(event)
        return event


class CommandAdd(CLICommand):

    keyword = 'add'
    help = 'adds a character to the battlefield'

    def _process_event(self, event):
        entity_name = self.get_arg_or_select_from_list(
            'Select character to add: ', get_character_library().keys())
        StateManager.add_character(entity_name)
        return event


class CommandMove(CLICommand):

    keyword = 'move'
    help = 'Calculate movement for attacker'
    required_keys = []

    def _process_event(self, event):
        event_copy = self.smart_select_attacker(event)
        attacker = choose_or_build_attacker(event_copy)
        move_opts = attacker.movement
        LOG.info('[(%s) - Movement: %s/%s/%s/%s]',
                 attacker.name,
                 move_opts.get(HALF_MOVE),
                 move_opts.get(FULL_MOVE),
                 move_opts.get(CHARGE_MOVE),
                 move_opts.get(RUN_MOVE))
        return event


class CommandTest(CLICommand):

    keyword = 'test'
    help = 'Test a skill or characteristic'
    required_keys = []

    def _process_event(self, event):
        attacker = choose_or_build_attacker(event)
        options = {}
        options.update(attacker.available_skills)
        options.update(attacker.effective_characteristics)
        test_stat = self.get_arg_or_select_from_list(
            'Select stat to test: ', options.keys())
        LOG.info('%s tests "%s"', attacker.name, test_stat)
        base_target = options.get(test_stat, 0)
        modifier = get_effective_modifier(event, manual_only=True)
        roll_target = base_target + modifier
        try_action(roll_target)
        return event


class CommandDefend(CLICommand):

    keyword = 'defend'
    help = 'Attacker attempts defensive actions.'
    required_keys = []

    def _process_event(self, event):
        event_copy = self.smart_select_attacker(event)
        handler_defend(event_copy)
        return event


class CommandScatter(CLICommand):

    keyword = 'scatter'
    help = 'Roll on scatter diagram.'

    def _process_event(self, event):
        scatter()
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
        bonus_value = self.get_arg_or_input_int('Enter bonus: ')
        event = add_roll_mod(event, bonus_value)
        return event


class CommandMalus(CLICommand):

    keyword = 'malus'
    help = 'Add a to-hit malus'

    def _process_event(self, event):
        malus_value = -self.get_arg_or_input_int('Enter malus: ')
        event = add_roll_mod(event, malus_value)
        return event


class ComandAdHoc(CLICommand):

    keyword = 'adhoc'
    help = 'Manually add temporary modifiers.'

    def _process_event(self, event):
        input_string = self.get_arg_or_input_string(
            'Enter ad-hoc dict string: ')
        ad_hoc_dict = quick_dict_parse(input_string)
        event = update_adhoc_dict(event, ad_hoc_dict)
        return event


class CommandRun(CLICommand):

    keyword = ''
    required_keys = [ATTACKER, TARGET, WEAPON, ROLL_TARGET]
    help = 'Roll attacks for the current event.'

    def _process_event(self, event):
        event = handler_run(event)
        return event


class CommandReload(CLICommand):

    keyword = 'reload'
    help = 'Reload character & weapon libraries.'

    def _process_event(self, event):
        MasterLibrary.reload_libraries()
        return event


class CommandInfo(CLICommand):

    keyword = 'info'
    required_keys = []
    help = 'Show talents & traits for character.'

    def _process_event(self, event):
        event_copy = self.smart_select_attacker(event)
        handler_info(event_copy)
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
        prompt = 'Choose package to load:'
        known_packages = MasterLibrary.get_known_packages()
        loaded_packages = MasterLibrary.get_loaded_packages()
        non_loaded_packages = [
            package for package in known_packages if package not in loaded_packages]
        package_name = self.get_arg_or_select_from_list(
            prompt, non_loaded_packages)
        MasterLibrary.add_package(package_name)
        return event


class CommandEquip(CLICommand):

    keyword = 'equip'
    help = 'Choose weapon from a list of available weapons.'

    def _process_event(self, event):
        weapon_name = try_user_choose_from_list(get_weapon_library().keys())
        event[WEAPON] = weapon_name
        event = handler_equip(event)
        return event


class CommandNew(CLICommand):

    keyword = 'new'
    help = 'Configure new attack.'

    def _process_event(self, event):
        event = handler_new(event)
        return event


class CommandAttacker(CLICommand):

    keyword = 'attacker'
    help = 'Choose attacker from a list of available characters.'

    def _process_event(self, event):
        event = self.smart_select_attacker(event)
        attacker_magnitude = try_user_input_int('Attacker magnitude: ')
        if attacker_magnitude is not None:
            event[ATTACKER_MAG] = attacker_magnitude
        return event


class CommandTarget(CLICommand):

    keyword = 'target'
    help = 'Choose target from a list of available characters.'

    def _process_event(self, event):
        event = self.smart_select_target(event)
        target_magnitude = try_user_input_int('Target magnitude: ')
        if target_magnitude is not None:
            event[TARGET_MAG] = target_magnitude
        return event


class CommandOverload(CLICommand):

    keyword = 'overload'
    help = 'Toggle overload TRUE/FALSE for current event.'

    def _process_event(self, event):
        event = self._toggle_key(OVERLOADED, event)
        return event


class CommandHelpless(CLICommand):

    keyword = 'helpless'
    help = 'Toggle helpless TRUE/FALSE for current event'

    def _process_event(self, event):
        event = self._toggle_adhoc_key(HELPLESS, event, True)
        return event


class CommandRange(CLICommand):

    keyword = 'range'
    help = 'Set range to target and update hit modifiers.'
    required_keys = [WEAPON]

    def _process_event(self, event):
        range_ = self.get_arg_or_input_int('Enter range to target: ')
        event[RANGE] = range_
        event = handler_range(event)
        return event


class CommandCover(CLICommand):

    keyword = 'cover'
    help = 'Add cover to the current event.'

    def _process_event(self, event):
        armor_value = self.get_arg_or_input_int('Enter cover armor value: ')
        event = self._toggle_adhoc_key(COVER, event, armor_value)
        return event


class CommandCharge(CLICommand):

    keyword = 'charge'
    help = 'Toggle charge TRUE/FALSE for current event.'
    required_keys = [ATTACKER]

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
    required_keys = [WEAPON]

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
        state_name = self.get_arg_or_input_string('Save state as: ')
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
        state_name = self.get_arg_or_input_string('Load which state? ')
        clean_state_name = normalize_string(state_name)
        state = SaveManager.load_state(clean_state_name)
        return state


class CommandDamage(CLICommand):

    keyword = 'damage'
    help = 'Manually enter the total damage of hits and calculate effective damage.'
    required_keys = [TARGET]

    def _process_event(self, event):
        damage = 0
        hits = []
        roll_result = user_input_int('Enter roll result: ')
        penetration = user_input_int('Enter penetration: ')
        event[ROLL_RESULT] = roll_result
        attack = build_base_attack(event)
        attack.roll_result = roll_result
        hitloc_iterator = build_hitloc_iterator(attack.hit_location)

        while damage != '':
            damage = raw_input('Enter damage: ')
            if damage == '':
                continue
            hit = Hit(hitloc_iterator.next(), damage, penetration)
            hits.append(hit)
        StateManager.update(event)
        attack.apply_hits(hits=hits)
        present_metadata(attack.metadata)
        log_messages()
        return event


class CommandAuto(CLICommand):

    keyword = 'auto'
    help = 'Auto configure event based on attacker.'
    required_keys = []

    def _process_event(self, event):
        event = handler_auto(event)
        return event


class CommandClear(CLICommand):

    keyword = 'clear'
    help = 'Clear the current event.'

    def _process_event(self, event):
        event.clear()
        return event


class CommandDos(CLICommand):

    keyword = 'dos'
    help = 'Calculate DoS'

    def _process_event(self, event):
        event_copy = deepcopy(event)
        result = user_input_int('Enter roll result: ')
        target = user_input_int('Enter roll target: ')
        event_copy[ROLL_RESULT] = result
        event_copy[ROLL_TARGET] = target
        attack = build_attack(event_copy)
        dos = attack.degrees_of_success
        semi_hits = 1 + int(dos / 2)
        fab_hits = 1 + dos
        LOG.info('%s vs %s = %s DoS', result, target, dos)
        LOG.info('SEMI/SWIFT Hits max: %s', semi_hits)
        LOG.info('FAB/LIGHTNING Hits max: %s', fab_hits)
        return event


class CommandProfile(CLICommand):

    keyword = 'profile'
    required_keys = []
    help = 'Show unit profile'

    def _process_event(self, event):
        event_copy = self.smart_select_attacker(event)
        handler_profile(event_copy)
        return event


class CommandRawDef(CLICommand):

    keyword = 'raw'
    required_keys = []
    help = 'Show raw definition'

    def _process_event(self, event):
        event_copy = self.smart_select_attacker(event)
        handler_rawdef(event_copy)
        return event
