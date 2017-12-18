from src.dwca_log.log import get_log


LOG = get_log(__name__)

REGISTER = {}


class Modifier(object):

    # pylint: disable=R0201
    name = None
    message = 'No message.'

    def modify_damage(self, attack, current_damage):
        _ = attack
        return current_damage

    def modify_penetration(self, attack, current_penetration):
        _ = attack
        return current_penetration

    def modify_num_dice(self, attack, current_num_dice):
        _ = attack
        return current_num_dice

    def modify_tearing_dice(self, attack, current_tearing_dice):
        _ = attack
        return current_tearing_dice

    def modify_num_hits(self, attack, current_num_hits):
        _ = attack
        return current_num_hits

    def add_to_metadata(self, attack):
        attack.add_modifier_effect_to_metadata(self.name, self.message)

    def on_hit(self, attack):
        _ = attack
        pass

    def on_damage(self, attack, effective_damage):
        _ = attack
        return effective_damage

    def modify_armor(self, attack, current_armor):
        _ = attack
        return current_armor


def register_modifiers():
    known_modifiers = [cls()
                       for cls in Modifier.__subclasses__()]  # pylint: disable=E1101

    for modifier in known_modifiers:
        add_to_register(modifier)


def add_to_register(modifier):
    key = modifier.name
    LOG.debug('Added modifier "%s" to registry.', key)
    REGISTER[key] = modifier


def get_modifiers_iterator(modifiers_dict):
    for modifier_name in modifiers_dict:
        modifier = get_modifier(modifier_name)
        if modifier is not None:
            yield modifier


def get_modifier(modifier_name):
    modifier = REGISTER.get(modifier_name)
    if modifier is None:
        LOG.debug('Modifier "%s" not available in register.', modifier_name)
    else:
        LOG.debug('Found modifier "%s"', modifier_name)
    return modifier
