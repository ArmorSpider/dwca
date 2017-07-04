from src.dwca_log.log import get_log

LOG = get_log(__name__)


class GoalRoll(object):

    def __init__(self, roll_result, target):
        self.roll_result = roll_result
        self.target = target

    def is_successfull(self):
        result = self.roll_result <= self.target
        LOG.debug('Is roll_result {} vs {} successfull: {}'.format(
            self.roll_result, self.target, result))
        return result

    def get_degrees_of_success(self):
        if self.is_successfull() is True:
            dos = int((self.target - self.roll_result) / 10)
        else:
            dos = 0
        LOG.debug('GoalRoll has {} DoS'.format(dos))
        return dos
