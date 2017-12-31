from definitions import ATTACKER, TARGET
from src.cli.auto_module import auto_assemble
from src.dwca_log.log import get_log
from src.entities.libraries import get_character_library
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def new_module(event):
    event.clear()
    LOG.info('Select attacker: ')
    character_name = try_user_choose_from_list(
        get_character_library().keys())
    event[ATTACKER] = character_name
    LOG.info('Select target: ')
    character_name = try_user_choose_from_list(
        get_character_library().keys())
    event[TARGET] = character_name
    event = auto_assemble(event)
    return event
