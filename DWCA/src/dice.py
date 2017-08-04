from src.dwca_log.log import get_log
from src.util.rand_util import roll_die


LOG = get_log(__name__)


def roll_action_dice():
    return roll_die(100)


def roll_damage_dice(num_dice):
    results = []
    for _ in range(num_dice):
        result = roll_die(10)
        results.append(result)
    LOG.debug('Rolled %s dice, results: %s', num_dice, results)
    return results
