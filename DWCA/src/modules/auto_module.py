from definitions import WEAPON,\
    ROLL_MODIFIERS
from src.dwca_log.log import get_log
from src.handler import choose_or_build_attacker
from src.modules.equip_module import handler_equip
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def handler_auto(event):
    event.pop(ROLL_MODIFIERS, None)
    attacker = choose_or_build_attacker(event)
    weapon_name = try_user_choose_from_list(attacker.weapons)
    event[WEAPON] = weapon_name
    event = handler_equip(event)
    return event
