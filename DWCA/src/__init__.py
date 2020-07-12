from src.dwca_log.log import get_log, create_log, add_console_handler
from src.modifiers.modifier import register_modifiers

LOG = create_log("dwca")
add_console_handler(LOG)
register_modifiers()

RULESET = "dw"
