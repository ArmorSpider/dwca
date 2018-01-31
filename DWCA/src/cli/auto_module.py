from definitions import FIREMODE, WEAPON, NUM_ATTACKS, ROLL_TARGET, RANGE,\
    ROLL_MODIFIERS
from src.dwca_log.log import get_log
from src.entities import SEMI_AUTO, FULL_AUTO, SINGLE_SHOT
from src.entities.char_stats import STAT_WS, STAT_BS, STAT_WIL
from src.errors import OutOfRangeError
from src.handler import build_attacker, build_weapon, build_target, build_base_attack,\
    choose_or_build_attacker
from src.modifiers.roll_modifier import ROF_MOD,\
    TWIN_LINKED_MOD, RANGE_MOD, add_roll_mod, SIZE_MOD, PSY_RATING_MOD,\
    SKILL_BONUS_MOD, HUNTER_OF_ALIENS_MOD, SLAYER_OF_DAEMONS_MOD
from src.modifiers.states import Push, Fettered, Unfettered
from src.util.event_util import update_adhoc_dict
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def auto_assemble(event):
    event.pop(ROLL_MODIFIERS, None)
    attacker = choose_or_build_attacker(event)
    weapon_name = try_user_choose_from_list(attacker.weapons)
    event[WEAPON] = weapon_name
    event = equip_weapon(event)
    return event


def equip_weapon(event):
    attacker = build_attacker(event)
    weapon = build_weapon(event)
    if weapon.is_melee():
        num_attacks = attacker.num_melee_attacks
        roll_target = attacker.get_characteristic(STAT_WS)
    elif weapon.is_psychic():
        num_attacks = 1
        roll_target = attacker.get_characteristic(STAT_WIL)
    else:
        num_attacks = attacker.num_ranged_attacks
        roll_target = attacker.get_characteristic(STAT_BS)
    event = calculate_hit_bonuses(event)
    event[NUM_ATTACKS] = num_attacks
    event[ROLL_TARGET] = roll_target
    return event


def calculate_hit_bonuses(event):
    attack = build_base_attack(event)
    if attack.is_psychic():
        event = pr_bonus_module(event)
    else:
        if attack.is_melee():
            if attack.hunter_of_aliens is not None and attack.target.is_alien():
                event = add_roll_mod(event, 10, HUNTER_OF_ALIENS_MOD)
            if attack.slayer_of_daemons is not None and attack.target.is_daemon():
                event = add_roll_mod(event, 10, SLAYER_OF_DAEMONS_MOD)
        if attack.is_ranged():
            if attack.weapon.twin_linked is not None:
                event = add_roll_mod(event, 20, TWIN_LINKED_MOD)
                LOG.info('+20 to hit from twin-linked.')
            event = firemode_module(event)
            event = range_module(event)

        event = size_module(event)
        if attack.weapon.skill_bonus is not None:
            event = add_roll_mod(
                event, attack.weapon.skill_bonus, SKILL_BONUS_MOD)
    return event


def pr_bonus_module(event):
    LOG.info('Choose power level: ')
    power_level = try_user_choose_from_list(
        [Push.name, Fettered.name, Unfettered.name])
    event = update_adhoc_dict(event, {power_level: True})

    attack = build_base_attack(event)
    psy_rating = attack.effective_psy_rating if attack.effective_psy_rating is not None else 0
    pr_bonus = psy_rating * 5
    LOG.info('+%s from effective psy rating. (%s)',
             pr_bonus, psy_rating)
    event = add_roll_mod(event, pr_bonus, PSY_RATING_MOD)
    return event


def size_module(event):
    target = build_target(event)
    event = add_roll_mod(event, target.size_bonus, SIZE_MOD)
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
        raise OutOfRangeError('%s is above weapon max range.' % range_)


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
