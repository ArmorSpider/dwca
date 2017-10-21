from src.dice import roll_damage_dice
from src.dwca_log.log import get_log
from src.entities import SINGLE_SHOT
from src.modifiers.qualities import Reliable, NeverJams, OverHeats


LOG = get_log(__name__)


def is_attack_auto_failed(attack):
    if is_eligible_for_jam(attack):
        if is_weapon_jammed(attack):
            LOG.info('%s has jammed!', attack.weapon)
            OverHeats.handle_overheats(attack)
        return True
    else:
        return False


def is_weapon_jammed(attack):
    if is_eligible_for_jam(attack):
        if attack.weapon.get_quality(NeverJams.name):
            return False
        elif attack.weapon.get_quality(Reliable.name):
            return _did_reliable_jam()
        else:
            return True
    else:
        return False


def get_jam_threshold(attack):
    if attack.weapon.get_quality(OverHeats.name):
        jam_threshold = 91
    else:
        jam_threshold = 96 if attack.firemode == SINGLE_SHOT else 94
    return jam_threshold


def is_eligible_for_jam(attack):
    return attack.roll_result >= get_jam_threshold(attack)


def _did_reliable_jam():
    reliable_roll = roll_damage_dice(1)[0]
    return reliable_roll == 10
