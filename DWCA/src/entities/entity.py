from src.dwca_log.log import get_log

LOG = get_log(__name__)


class Entity(object):

    def __init__(self, definition=None):
        self.definition = definition

    def __str__(self, *args, **kwargs):
        return self.get_name()

    def get_definition(self):
        return self.definition

    def get_name(self):
        return str(self.get_stat('name'))

    def get_stat(self, stat_name, default=None):
        LOG.debug('Getting stat "%s"', stat_name)
        result = self.get_definition().get(stat_name, default)
        LOG.debug('%s = %s', stat_name, result)
        return result
