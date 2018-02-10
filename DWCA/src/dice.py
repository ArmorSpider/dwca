from src.dwca_log.log import get_log
from src.util.rand_util import roll_die


LOG = get_log(__name__)

QUEUED_ROLLS_D10 = []
QUEUED_ROLLS_D100 = []


def roll_action_dice():
    if len(QUEUED_ROLLS_D100) > 0:
        result = QUEUED_ROLLS_D100.pop()
    else:
        result = roll_die(100)
    return result


def roll_damage_die():
    return roll_die(10)


def roll_damage_dice(num_dice):
    results = []
    for _ in range(num_dice):
        if len(QUEUED_ROLLS_D10) > 0:
            result = QUEUED_ROLLS_D10.pop(0)
        else:
            result = roll_die(10)
        results.append(result)
    LOG.debug('Rolled %s dice, results: %s', num_dice, results)
    return results


def queue_d10_rolls(list_of_ints):
    del QUEUED_ROLLS_D10[:]
    QUEUED_ROLLS_D10.extend(list_of_ints)


def queue_d100_rolls(list_of_ints):
    del QUEUED_ROLLS_D100[:]
    QUEUED_ROLLS_D100.extend(list_of_ints)
