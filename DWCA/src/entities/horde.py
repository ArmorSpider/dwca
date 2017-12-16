from src.dwca_log.log import get_log
from src.entities.character import Character
from src.entities.libraries import read_character
from src.modifiers.qualities import Devastating, Hellfire
from src.util.rand_util import get_tens


LOG = get_log(__name__)


def get_horde(creature_name, magnitude):
    char_definition = read_character(creature_name)
    horde = Horde(char_definition, magnitude)
    return horde


class Horde(Character):

    def __init__(self, definition=None, magnitude=1):
        Character.__init__(self, definition=definition)
        self.magnitude = int(magnitude)

    def is_horde(self):
        return True

    def get_num_ranged_attacks(self):
        num_attacks = get_tens(self.magnitude)
        if self.fire_drill is not None:
            num_attacks += 1
        LOG.info('%s can make %s ranged attacks.', self, num_attacks)
        return num_attacks

    def mitigate_hit(self, attack, hit):
        effective_damage = super(Horde, self).mitigate_hit(attack, hit)
        magnitude_damage = min(1, effective_damage)
        magnitude_damage = Devastating.handle_devastating(
            attack, magnitude_damage)
        magnitude_damage = Hellfire.handle_hellfire_magnitude_damage(
            attack, magnitude_damage)
        LOG.info('Magnitude damage: %s', magnitude_damage)
        return magnitude_damage
