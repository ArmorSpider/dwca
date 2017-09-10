from definitions import PROTECTION_MAX, OVERLOAD_MAX
from src.dice import roll_action_dice
from src.dwca_log.log import get_log
from src.state_manager import is_overloaded

LOG = get_log(__name__)


class ForceField(object):

    def __init__(self, definition):
        self.protection_max = definition[PROTECTION_MAX]
        self.overload_max = definition[OVERLOAD_MAX]
        self.overloaded = False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def is_hit_blocked(self, roll_result=None):
        if roll_result is None:
            roll_result = roll_action_dice()
        result = self._is_roll_result_blocked(roll_result)
        LOG.debug('Did force field block? %s (%s vs. %s)',
                  result, roll_result, self.protection_max)
        return result

    def _is_roll_result_blocked(self, roll_result):
        if self.overloaded is True or is_overloaded() is True:
            LOG.debug('Force field is overloaded.')
            return False
        else:
            if roll_result <= self.overload_max:
                self.overloaded = True
                LOG.info('Force field overloaded! (%s vs. %s)',
                         roll_result, self.overload_max)
            if roll_result <= self.protection_max:
                return True
            return False
