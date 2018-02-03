from src.dwca_log.log import get_log
from src.entities.character import Character
from src.entities.libraries import read_character
from src.util.rand_util import get_tens


LOG = get_log(__name__)


def get_horde(creature_name, magnitude):
    char_definition = read_character(creature_name)
    horde = Horde(char_definition, magnitude)
    return horde


class Horde(Character):

    def __init__(self, definition=None, magnitude=1):
        super(Horde, self).__init__(definition=definition)
        self.magnitude = int(magnitude)

    def is_horde(self):
        return True

    @property
    def name(self):
        base_name = super(Horde, self).name
        horde_name = 'Horde of {mag} {name}s'.format(
            mag=self.magnitude, name=base_name)
        return horde_name

    @property
    def num_ranged_attacks(self):
        num_attacks = get_tens(self.magnitude)
        if self.fire_drill is not None:
            num_attacks += 1
        LOG.info('%s can make %s ranged attacks.', self, num_attacks)
        return num_attacks

    @property
    def size_bonus(self):
        size_bonus = super(Horde, self).size_bonus
        if self.magnitude >= 30:
            size_bonus += 30
        if self.magnitude >= 60:
            size_bonus += 10
        if self.magnitude >= 90:
            size_bonus += 10
        if self.magnitude >= 120:
            size_bonus += 10
        return size_bonus
