from src.dwca_log.log import get_log

MESSAGE_QUEUE = []

LOG = get_log(__name__)


def queue_message(message):
    MESSAGE_QUEUE.append(message)


def log_messages():
    if len(MESSAGE_QUEUE) > 0:
        LOG.info('________[EXTRA EFFECTS]________')
    for message in MESSAGE_QUEUE:
        LOG.info(message)
    del MESSAGE_QUEUE[:]


def clear_messages():
    del MESSAGE_QUEUE[:]
