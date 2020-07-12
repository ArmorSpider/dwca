from copy import deepcopy

from src.dwca_log.log import get_log
from src.entities.libraries import find_best_match


LOG = get_log(__name__)


class SaveManager(object):

    saved_states = {}

    @staticmethod
    def save_state(state_name, event):
        try:
            SaveManager.saved_states[state_name] = deepcopy(event)
        except Exception:
            LOG.error('Save state failed.')
        else:
            LOG.info('Saved state as "%s".', state_name)

    @staticmethod
    def load_state(state_name):
        available_states = list(SaveManager.saved_states.keys())
        state_name_best_match = find_best_match(state_name, available_states)
        state = deepcopy(SaveManager.saved_states[state_name_best_match])
        return state
