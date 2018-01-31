from src.cli.message_queue import log_messages
from src.dwca_log.log import get_log
from src.handler import main_handler
from src.situational.state_manager import StateManager


LOG = get_log(__name__)


def run_module(event):
    StateManager.update(event)
    main_handler(event)
    log_messages()
    return event
