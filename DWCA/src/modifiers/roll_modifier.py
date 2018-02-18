from definitions import ROLL_MODIFIERS
from src.dwca_log.log import get_log

OTHER_MODS = 'other_mods'
SIZE_MOD = 'size_mod'
RANGE_MOD = 'range_mod'
CHARGE_MOD = 'charge_mod'
AIM_MOD = 'aim_mod'
TWIN_LINKED_MOD = 'twin_linked_mod'
ATTACK_MODE_MOD = 'attack_mode_mod'
PSY_RATING_MOD = 'psy_rating_mod'
SKILL_BONUS_MOD = 'skill_bonus_mod'
HUNTER_OF_ALIENS_MOD = 'hunter_of_aliens_mod'
SLAYER_OF_DAEMONS_MOD = 'slayer_of_daemons_mod'


LOG = get_log(__name__)


class RollModifier(object):

    def __init__(self, modifier_value, unique_key=None):
        assert isinstance(modifier_value, int)
        self.value = modifier_value
        self.key = unique_key if unique_key is not None else OTHER_MODS


def add_roll_mod(event, value, unique_key=None):
    roll_modifier = RollModifier(modifier_value=value, unique_key=unique_key)
    event = add_roll_modifier(event, roll_modifier)
    return event


def add_roll_modifier(event, roll_modifier):
    roll_modifiers = event.get(ROLL_MODIFIERS, {})
    modifier_values = []
    if roll_modifier.key == OTHER_MODS:
        modifier_values.extend(roll_modifiers.get(roll_modifier.key, []))
    modifier_values.append(roll_modifier.value)

    if roll_modifiers.get(roll_modifier.key) == modifier_values:
        roll_modifiers.pop(roll_modifier.key)
    else:
        roll_modifiers[roll_modifier.key] = modifier_values
    event[ROLL_MODIFIERS] = roll_modifiers
    return event


def get_effective_modifier(event, manual_only=False):
    roll_modifiers = event.get(ROLL_MODIFIERS, {})
    effective_modifier = 0
    for key, modifier_values in roll_modifiers.iteritems():
        if manual_only is True and key != OTHER_MODS:
            continue
        key_total = sum(modifier_values)
        LOG.debug('%s from "%s".', key_total, key)
        effective_modifier += key_total
    effective_modifier = enforce_modifier_cap(effective_modifier)
    return effective_modifier


def enforce_modifier_cap(effective_modifier):
    if effective_modifier > 60:
        effective_modifier = 60
    elif effective_modifier < -60:
        effective_modifier = -60
    return effective_modifier
