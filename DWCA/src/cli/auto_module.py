from definitions import FIREMODE, WEAPON, NUM_ATTACKS, ROLL_TARGET
from src.dwca_log.log import get_log
from src.entities import SEMI_AUTO, FULL_AUTO
from src.entities.char_stats import STAT_WS, STAT_BS
from src.entities.weapon import get_weapon
from src.handler import build_attacker
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def auto_assemble(event):
    attacker = build_attacker(event)
    weapon_name = try_user_choose_from_list(attacker.weapons)
    weapon = get_weapon(weapon_name)
    if weapon.is_melee():
        num_attacks = attacker.get_num_melee_attacks()
        roll_target = attacker.get_characteristic(STAT_WS)
    else:
        num_attacks = attacker.get_num_ranged_attacks()
        roll_target = attacker.get_characteristic(STAT_BS)
        firemodes = weapon.firemodes.keys()
        firemode = try_user_choose_from_list(firemodes)
        if firemode == SEMI_AUTO:
            LOG.info('+10 to roll target from semi auto.')
            roll_target += 10
        elif firemode == FULL_AUTO:
            LOG.info('+20 to roll target from full auto.')
            roll_target += 20
        if weapon.twin_linked is not None:
            LOG.info('+20 to roll target from twin-linked.')
            roll_target += 20
        event[FIREMODE] = firemode
    event[WEAPON] = weapon_name
    event[NUM_ATTACKS] = num_attacks
    event[ROLL_TARGET] = roll_target
    return event
