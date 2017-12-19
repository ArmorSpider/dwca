import json

from src.cli.commands import process_command
from src.dwca_log.log import get_log
from src.errors import NoMatchError, ChooseFromListFailedError

LOG = get_log(__name__)

SAVED_STATES = {}


def cli_loop():
    event = {}
    while True:
        _cleanup_event(event)
        _display_event(event)
        command_string = raw_input('Enter commands: \n')
        try:
            event = process_command(command_string, event)
        except (ValueError, NoMatchError, ChooseFromListFailedError) as error:
            LOG.error(error.message)


def _display_event(event):
    print '[CURRENT EVENT]'
    print json.dumps(event, indent=4)


def _cleanup_event(event):
    for key, value in event.items():
        if not value:
            event.pop(key)
        elif key.startswith('_'):
            event.pop(key)


def main():
    cli_loop()


if __name__ == '__main__':
    main()
