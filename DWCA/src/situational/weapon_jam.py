from src.dice import roll_damage_dice
from src.entities import SINGLE_SHOT
from src.modifiers.qualities import Reliable, NeverJams


def is_weapon_jammed(attack):
    if _is_eligible_for_jam(attack):
        if attack.weapon.get_quality(NeverJams.name):
            return False
        elif attack.weapon.get_quality(Reliable.name):
            return _did_reliable_jam()
        else:
            return True
    else:
        return False


def get_jam_threshold(firemode):
    jam_threshold = 96 if firemode == SINGLE_SHOT else 94
    return jam_threshold


def _is_eligible_for_jam(attack):
    return attack.roll_result >= get_jam_threshold(attack.firemode)


def _did_reliable_jam():
    reliable_roll = roll_damage_dice(1)[0]
    return reliable_roll == 10
