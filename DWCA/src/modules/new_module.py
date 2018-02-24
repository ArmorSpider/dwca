from definitions import ATTACKER, TARGET
from src.dwca_log.log import get_log
from src.modules.auto_module import handler_auto
from src.situational.state_manager import StateManager
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def handler_new(event):
    event.clear()
    LOG.info('Select attacker: ')
    character_name = try_user_choose_from_list(
        StateManager.available_characters())
    event[ATTACKER] = character_name
    LOG.info('Select target: ')
    character_name = try_user_choose_from_list(
        StateManager.available_characters())
    event[TARGET] = character_name
    event = handler_auto(event)
    return event
