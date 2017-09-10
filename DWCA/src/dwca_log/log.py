import logging
import sys

DEFAULT_CONSOLE_LOG_LEVEL = logging.INFO


def get_log(log_name):
    full_log_name = 'dwca.{}'.format(log_name)
    return create_log(full_log_name)


def create_log(log_name, log_level=DEFAULT_CONSOLE_LOG_LEVEL):
    new_log = logging.getLogger(str(log_name))
    new_log.setLevel(log_level)
    if log_name == '__builtin__':
        add_console_handler(new_log, log_level)
    return new_log


def add_console_handler(log, log_level=DEFAULT_CONSOLE_LOG_LEVEL):
    if len(log.handlers) == 0:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = _get_standard_formatter()
        handler.setFormatter(formatter)
        log.addHandler(handler)


def _get_standard_formatter():
    return CustomFormatter()


class CustomFormatter(logging.Formatter):

    detailed_formatting = '[%(levelname)s] - %(message)-120s (%(name)s.%(funcName)s:%(lineno)d)'
    error_formatting = detailed_formatting
    debug_formatting = '[%(levelname)s] %(message)s'
    warning_formatting = detailed_formatting
    info_formatting = '%(message)s'

    def __init__(self, fmt='[%(asctime)s] [%(levelname)s] - %(message)s'):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        original_format = self._fmt
        if record.levelno == logging.DEBUG:
            self._fmt = CustomFormatter.debug_formatting
        elif record.levelno == logging.INFO:
            self._fmt = CustomFormatter.info_formatting
        elif record.levelno == logging.ERROR:
            self._fmt = CustomFormatter.error_formatting
        elif record.levelno == logging.WARNING:
            self._fmt = CustomFormatter.warning_formatting
        result = logging.Formatter.format(self, record)
        self._fmt = original_format
        return result
