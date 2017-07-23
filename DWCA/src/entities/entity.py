from src.dwca_log.log import get_log

LOG = get_log(__name__)


class Entity(object):

    def __init__(self, definition=None):
        self.definition = definition

    def get_definition(self):
        return self.definition

    def get_stat(self, stat_name):
        LOG.debug('Getting stat "{}"'.format(stat_name))
        result = self.get_definition().get(stat_name)
        LOG.debug('{} = {}'.format(stat_name, result))
        return result
