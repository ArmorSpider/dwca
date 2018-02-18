from __future__ import division

from copy import deepcopy

from definitions import NUM_ATTACKS, ROLL_TARGET, ROLL_MODIFIERS, WEAPON,\
    FIREMODE
from src.dwca_log.log import get_log
from src.handler import choose_or_build_attacker, build_weapon
from src.modules.run_module import main_handler


LOG = get_log(__name__)


def handler_dps(event):
    dps_event = deepcopy(event)
    dps_event[NUM_ATTACKS] = 500
    dps_event[ROLL_TARGET] = 100
    dps_event[ROLL_MODIFIERS] = {}
    attack_damages = main_handler(dps_event)
    total_damage = sum(attack_damages)
    total_attacks = len(attack_damages)
    damaging_attacks = 0
    failed_attacks = 0
    for attack_damage in attack_damages:
        if attack_damage > 0:
            damaging_attacks += 1
        else:
            failed_attacks += 1
    try:
        damage_per_successfull_attack = total_damage / damaging_attacks
    except ZeroDivisionError:
        damage_per_successfull_attack = 0
    hitrate = damaging_attacks / total_attacks
    LOG.info('RESULT: %s%% chance for %s damage.', hitrate *
             100, damage_per_successfull_attack)
    return event
