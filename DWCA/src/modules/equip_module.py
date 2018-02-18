from definitions import NUM_ATTACKS, ROLL_TARGET
from src.dwca_log.log import get_log
from src.entities.char_stats import STAT_WS, STAT_WIL, STAT_BS
from src.handler import build_attacker, build_weapon, build_base_attack
from src.modifiers.roll_modifier import add_roll_mod, HUNTER_OF_ALIENS_MOD,\
    SLAYER_OF_DAEMONS_MOD, TWIN_LINKED_MOD, SKILL_BONUS_MOD
from src.modules.firemode_module import handler_firemode
from src.modules.pr_module import handler_pr_bonus
from src.modules.range_module import handler_range
from src.modules.size_module import handler_size


LOG = get_log(__name__)


def handler_equip(event):
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
        event = handler_pr_bonus(event)
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
            event = handler_range(event)
        event = handler_firemode(event)
        event = handler_size(event)
        if attack.weapon.skill_bonus is not None:
            event = add_roll_mod(
                event, attack.weapon.skill_bonus, SKILL_BONUS_MOD)
    return event
