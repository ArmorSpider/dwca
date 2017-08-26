from src.dwca_log.log import get_log
from src.util.rand_util import roll_die


LOG = get_log(__name__)

QUEUED_ROLLS = []


def roll_action_dice():
    return roll_die(100)


def roll_damage_dice(num_dice):
    results = []
    for _ in range(num_dice):
        if len(QUEUED_ROLLS) > 0:
            result = QUEUED_ROLLS.pop(0)
        else:
            result = roll_die(10)
        results.append(result)
    LOG.debug('Rolled %s dice, results: %s', num_dice, results)
    return results


def queue_rolls(list_of_ints):
    del QUEUED_ROLLS[:]
    QUEUED_ROLLS.extend(list_of_ints)
