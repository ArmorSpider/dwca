from src.dwca_log.log import get_log

LOG = get_log(__name__)


class GoalRoll(object):

    def __init__(self, _roll_dice, target):
        self._roll_dice = _roll_dice
        self.target = target

    def is_successfull(self):
        result = self._roll_dice <= self.target
        LOG.debug('Is _roll_dice {} vs {} successfull: {}'.format(
            self._roll_dice, self.target, result))
        return result

    def get_degrees_of_success(self):
        if self.is_successfull() is True:
            dos = int((self.target - self._roll_dice) / 10)
        else:
            dos = 0
        return dos
