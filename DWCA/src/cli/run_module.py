from src.cli.message_queue import log_messages
from src.handler import main_handler
from src.situational.state_manager import StateManager


def run_module(event):
    StateManager.update(event)
    main_handler(event)
    log_messages()
    return event
