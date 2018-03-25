from src.dwca_log.log import get_log
from src.entities import WOUNDS
from src.modifiers.modifier import get_modifier


LOG = get_log(__name__)


class Entity(object):

    def __getattr__(self, name):
        attribute = self.modifiers.get(name)
        if attribute is None and get_modifier(name) is None:
            return super(Entity, self).__getattribute__(name)
        else:
            return attribute

    def __init__(self, definition={}):
        self.definition = definition

    def __str__(self, *args, **kwargs):
        return self.name

    @property
    def wounds(self):
        return self.get_stat(WOUNDS, 0)

    @property
    def name(self):
        return str(self.get_stat('name', 'NAME_MISSING'))

    def get_stat(self, stat_name, default=None):
        LOG.log(5, 'Getting stat "%s"', stat_name)
        result = self.definition.get(stat_name, default)
        LOG.log(5, '%s = %s', stat_name, result)
        return result

    def is_horde(self):
        return False

    def is_vehicle(self):
        return False

    @property
    def modifiers(self):
        return {}
