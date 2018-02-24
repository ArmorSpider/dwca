from definitions import OVERLOADED, COVER
from src.dwca_log.log import get_log
from src.entities.libraries import get_character_library


LOG = get_log(__name__)


class StateManager(object):

    overloaded = False
    cover = 0
    extra_characters = []
    base_characters = get_character_library().keys()

    @staticmethod
    def get_loaded_characters():
        return StateManager.base_characters + StateManager.extra_characters

    @staticmethod
    def reset():
        StateManager.update({})

    @staticmethod
    def update(event):
        StateManager.overloaded = bool(event.get(OVERLOADED))
        StateManager.cover = int(event.get(COVER, 0))

    @staticmethod
    def add_character(entity_name):
        if entity_name not in StateManager.extra_characters:
            LOG.info('Added "%s" to battlefield.', entity_name)
            StateManager.extra_characters.append(entity_name)
        else:
            LOG.info('"%s" is already added.', entity_name)

    @staticmethod
    def remove_character(entity_name):
        LOG.info('Removing "%s" from battlefield.', entity_name)
        StateManager.extra_characters.remove(entity_name)

    @staticmethod
    def available_characters():
        if StateManager.get_loaded_characters() == StateManager.base_characters:
            return get_character_library().keys()
        else:
            return StateManager.get_loaded_characters()


def is_overloaded():
    return StateManager.overloaded


def get_cover():
    return StateManager.cover
