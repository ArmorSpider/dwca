from src.dice import roll_damage_dice, roll_action_dice
from src.dwca_log.log import get_log
from src.modifiers.talents import DeathwatchTraining
from src.modifiers.traits import TouchedByTheFates


LOG = get_log(__name__)


def roll_normal_damage(real_dice, tearing_dice):
    LOG.debug('Rolling damage with %s dice (%s tearing).',
              real_dice, tearing_dice)
    num_dice = real_dice + tearing_dice

    results = sorted(roll_damage_dice(num_dice))
    actual_results = results[-real_dice::]
    LOG.debug('Rolled normal damage: %s', actual_results)
    return actual_results


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
    return attack.get_attacker().get_talent(DeathwatchTraining.name) or \
        attack.get_attacker().get_talent(TouchedByTheFates.name)


def is_fury_auto_confirmed(attack):
    return attack.get_attacker().get_talent(DeathwatchTraining.name) and \
        attack.get_target().is_alien()


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
