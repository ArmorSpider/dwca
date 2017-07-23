from src.dwca_log.log import get_log


LOG = get_log(__name__)

REGISTER = {}


class Modifier(object):

    def __init__(self):
        self.modifier_name = None

    def modify_damage(self, melee_attack, current_damage):
        return current_damage

    def modify_penetration(self, melee_attack, current_pen):
        return current_pen


def register_modifiers():
    known_modifiers = [cls() for cls in Modifier.__subclasses__()]
    for modifier in known_modifiers:
        add_to_register(modifier)


def add_to_register(modifier):
    global REGISTER
    key = modifier.modifier_name
    LOG.debug('Added modifier "{}" to registry.'.format(key))
    REGISTER[key] = modifier


def get_modifier(modifier_name):
    modifier = REGISTER.get(modifier_name)
    if modifier is None:
        LOG.debug(
            'Modifier "{}" not available in register.'.format(modifier_name))
        #LOG.debug('Available modifiers: {} '.format(REGISTER.keys()))
    else:
        LOG.debug('Found modifier "{}"'.format(modifier_name))
    return modifier
