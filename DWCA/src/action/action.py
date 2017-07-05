from src.dice import roll_action_dice
from src.dwca_log.log import get_log
from src.hit_location import get_hit_location
LOG = get_log(__name__)


def reverse_string(string_):
    return string_[::-1]


class Action(object):

    def __init__(self):
        self.roll_result = None
        self.roll_target = None

    def try_action(self, roll_target, roll_result=None):
        if roll_result is None:
            roll_result = roll_action_dice()
        self.roll_result = roll_result
        self.roll_target = roll_target

    def is_successfull(self):
        result = self.roll_result <= self.roll_target
        LOG.debug('Is roll_result {} vs {} successfull: {}'.format(
            self.roll_result, self.roll_target, result))
        return result

    def get_degrees_of_success(self):
        if self.is_successfull() is True:
            dos = int((self.roll_target - self.roll_result) / 10)
        else:
            dos = 0
        LOG.debug('Action has {} DoS'.format(dos))
        return dos

    def get_reverse(self):
        roll_string = str(self.roll_result)
        reversed_string = reverse_string(roll_string)
        if len(reversed_string) == 1:
            reversed_string += '0'
        return int(reversed_string)

    def get_hit_location(self):
        reversed_roll = self.get_reverse()
        hit_location = get_hit_location(reversed_roll)
        return hit_location
