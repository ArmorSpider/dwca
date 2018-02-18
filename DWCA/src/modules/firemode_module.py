from definitions import FIREMODE
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.handler import build_weapon
from src.modifiers.roll_modifier import add_roll_mod, ROF_MOD
from src.util.user_input import try_user_choose_from_list


def handler_firemode(event):
    event = _choose_firemode(event)
    firemode = event[FIREMODE]
    firemode_bonuses = {SINGLE_SHOT: 0,
                        SEMI_AUTO: 10,
                        FULL_AUTO: 20}
    firemode_bonus = firemode_bonuses[firemode]
    event = add_roll_mod(event, firemode_bonus, ROF_MOD)
    return event


def _choose_firemode(event):
    weapon = build_weapon(event)
    firemodes = weapon.firemodes.keys()
    firemode = try_user_choose_from_list(firemodes)
    event[FIREMODE] = firemode
    return event
