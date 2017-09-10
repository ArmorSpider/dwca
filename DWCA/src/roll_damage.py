from src.dice import roll_damage_dice, roll_action_dice
from src.dwca_log.log import get_log
from src.modifiers.qualities import Volatile, Proven
from src.modifiers.talents import DeathwatchTraining
from src.modifiers.traits import TouchedByTheFates


LOG = get_log(__name__)


def roll_normal_damage(real_dice, tearing_dice, attack=None):
    LOG.debug('Rolling damage with %s dice (%s tearing).',
              real_dice, tearing_dice)
    num_dice = real_dice + tearing_dice

    results = sorted(roll_damage_dice(num_dice))
    actual_results = results[-real_dice::]
    LOG.debug('Rolled normal damage: %s', actual_results)
    if attack is not None:
        actual_results = Proven.handle_proven(attack, actual_results)
        actual_results = handle_dos_minimum_damage(attack, actual_results)
    return actual_results


def handle_dos_minimum_damage(dos, roll_results):
    capped_dos = min(dos, 9)  # avoid righteous fury from DoS
    sorted_results_descending = sorted(roll_results, reverse=True)
    minimum_value = sorted_results_descending.pop()
    updated_value = max(capped_dos, minimum_value)
    sorted_results_descending.append(updated_value)
    resorted_results = sorted(sorted_results_descending, reverse=True)
    return resorted_results


def roll_righteous_fury(actual_results, attack):
    fury_possible = is_fury_possible(attack)
    fury_triggered = is_fury_triggered(actual_results)
    auto_confirm = is_fury_auto_confirmed(attack)
    if fury_triggered and fury_possible:
        righteous_fury(actual_results, attack, auto_confirm)
    return actual_results


def is_fury_triggered(actual_results):
    return 10 in actual_results


def is_fury_possible(attack):
    attacker = attack.get_attacker()
    return attacker.get_talent(DeathwatchTraining.name) or \
        attacker.get_talent(TouchedByTheFates.name)


def is_fury_auto_confirmed(attack):
    return (attack.get_attacker().get_talent(DeathwatchTraining.name) and
            attack.get_target().is_alien()) or attack.get_weapon().get_quality(Volatile.name) is not None


def righteous_fury(results, attack, auto_confirm):
    result = -1
    while result == 10 or result == -1:
        if auto_confirm or confirm_righteous_fury(attack):
            LOG.info('Triggered righteous fury!')
            result = roll_damage_dice(1).pop()
            results.append(result)
        else:
            result = None


def confirm_righteous_fury(attack):
    roll_target = attack.roll_target
    roll_result = roll_action_dice()
    result = roll_result <= roll_target
    LOG.debug('Did righteous fury confirm? %s (%s vs. %s)',
              result, roll_result, roll_target)
    return result
