from definitions import RANGE
from src.errors import OutOfRangeError
from src.handler import build_weapon
from src.modifiers.roll_modifier import add_roll_mod, RANGE_MOD


def handler_range(event):
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
