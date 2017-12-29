from definitions import FIREMODE, WEAPON, NUM_ATTACKS, ROLL_TARGET, RANGE,\
    ROLL_MODIFIERS
from src.dwca_log.log import get_log
from src.entities import SEMI_AUTO, FULL_AUTO, SINGLE_SHOT
from src.entities.char_stats import STAT_WS, STAT_BS
from src.errors import OutOfRangeError
from src.handler import build_attacker, build_weapon, build_target
from src.modifiers.roll_modifier import ROF_MOD,\
    TWIN_LINKED_MOD, RANGE_MOD, add_roll_mod, SIZE_MOD
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def auto_assemble(event):
    event.pop(ROLL_MODIFIERS, None)
    attacker = build_attacker(event)
    weapon_name = try_user_choose_from_list(attacker.weapons)
    event[WEAPON] = weapon_name
    weapon = build_weapon(event)
    if weapon.is_melee():
        num_attacks = attacker.get_num_melee_attacks()
        roll_target = attacker.get_characteristic(STAT_WS)
    else:
        num_attacks = attacker.get_num_ranged_attacks()
        roll_target = attacker.get_characteristic(STAT_BS)
        event = firemode_module(event)
        event = range_module(event)
        if weapon.twin_linked is not None:
            event = add_roll_mod(event, 20, TWIN_LINKED_MOD)
            LOG.info('+20 to roll target from twin-linked.')
    event = size_module(event)
    event[NUM_ATTACKS] = num_attacks
    event[ROLL_TARGET] = roll_target
    return event


def size_module(event):
    target = build_target(event)
    size_bonus = target.size_bonus
    event = add_roll_mod(event, size_bonus, SIZE_MOD)
    return event


def range_module(event):
    if RANGE in event:
        weapon = build_weapon(event)
        if weapon.is_melee() is False:
            range_ = event[RANGE]
            range_modifier = _get_range_modifier(range_, weapon.range_options)
            event = add_roll_mod(event, range_modifier, RANGE_MOD)
    return event


def _get_range_modifier(range_, range_options):
    range_limits = sorted(range_options.keys())
    for range_limit in range_limits:
        if range_ <= range_limit:
            range_modifier = range_options[range_limit]
            return range_modifier
    else:
        raise OutOfRangeError('%s is out of range.' % range_)


def firemode_module(event):
    event = choose_firemode(event)
    firemode = event[FIREMODE]
    firemode_bonuses = {SINGLE_SHOT: 0,
                        SEMI_AUTO: 10,
                        FULL_AUTO: 20}
    firemode_bonus = firemode_bonuses[firemode]
    event = add_roll_mod(event, firemode_bonus, ROF_MOD)
    return event


def choose_firemode(event):
    weapon = build_weapon(event)
    firemodes = weapon.firemodes.keys()
    firemode = try_user_choose_from_list(firemodes)
    event[FIREMODE] = firemode
    return event
