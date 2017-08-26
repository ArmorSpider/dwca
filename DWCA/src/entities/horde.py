from src.dwca_log.log import get_log
from src.entities.character import Character
from src.modifiers.qualities import Devastating
from src.modifiers.traits import FireDrill
from src.util.rand_util import get_tens
from src.util.read_file import read_character


LOG = get_log(__name__)


def get_horde(creature_name, magnitude):
    char_definition = read_character(creature_name)
    horde = Horde(char_definition, magnitude)
    return horde


class Horde(Character):

    def __init__(self, definition=None, magnitude=1):
        Character.__init__(self, definition=definition)
        self.magnitude = magnitude

    def is_horde(self):
        return True

    def get_magnitude(self):
        return self.magnitude

    def get_num_ranged_attacks(self):
        num_attacks = get_tens(self.get_magnitude())
        if self.get_trait(FireDrill.name):
            num_attacks += 1
        LOG.info('%s can make %s ranged attacks.', self, num_attacks)
        return num_attacks

    def mitigate_hit(self, attack, hit):
        armor = self.get_armor(hit.hit_location)
        toughness = self._get_effective_toughness_bonus(attack)
        effective_damage = hit.calculate_effective_damage(armor, toughness)
        magnitude_damage = min(1, effective_damage)
        devastating_value = attack.get_weapon().get_quality(Devastating.name)
        if devastating_value is not None:
            magnitude_damage += devastating_value
        return magnitude_damage
