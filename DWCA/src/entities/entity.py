from src.dwca_log.log import get_log

LOG = get_log(__name__)


class Entity(object):

    def __init__(self, definition={}):
        self.definition = definition

    def __str__(self, *args, **kwargs):
        return self.get_name()

    def get_name(self):
        return str(self.get_stat('name'))

    def get_stat(self, stat_name, default=None):
        LOG.log(5, 'Getting stat "%s"', stat_name)
        result = self.definition.get(stat_name, default)
        LOG.log(5, '%s = %s', stat_name, result)
        return result

    def is_horde(self):
        return False
