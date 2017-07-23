from src.action.melee_attack import MeleeAttack
from src.dwca_log.log import get_log
from src.entities import ARMOR, CHARACTERISTICS, TRAITS
from src.entities.entity import Entity
from src.hit_location import HITLOC_ALL
from src.util.rand_util import get_tens
from src.util.read_file import read_character


LOG = get_log(__name__)
UNDEFINED_ARMOR_VALUE = 0
UNDEFINED_CHARACTERISTIC_VALUE = 0
DEFAULT_CHARACTERISTIC_MULTIPLIER = 1


def get_char(char_name):
    char_definition = read_character(char_name)
    char = Character(char_definition)
    return char


class Character(Entity):

    def melee_attack(self, weapon, target=None):
        return MeleeAttack(weapon=weapon,
                           attacker=self,
                           target=target)

    def get_armor(self, hit_location):
        armor_dict = self._get_armor_definition()
        armor = armor_dict.get(hit_location)
        if armor is None:
            armor = armor_dict.get(HITLOC_ALL, UNDEFINED_ARMOR_VALUE)
        return armor

    def _get_armor_definition(self):
        return self.get_stat(ARMOR)

    def _get_characteristics(self):
        return self.get_stat(CHARACTERISTICS)

    def get_characteristic(self, characteristic):
        char_stats = self._get_characteristics()
        char_stat = char_stats.get(
            characteristic, UNDEFINED_CHARACTERISTIC_VALUE)
        return char_stat

    def get_characteristic_bonus(self, characteristic):
        characteristic_value = self.get_characteristic(characteristic)
        characteristic_bonus = get_tens(characteristic_value)
        characteristic_multiplier = self.get_characteristic_multiplier(
            characteristic)
        final_bonus = characteristic_bonus * characteristic_multiplier
        return final_bonus

    def get_trait(self, trait_name):
        traits = self.get_stat(TRAITS)
        trait_value = traits.get(trait_name)
        LOG.debug(
            'Found value "{}" for trait "{}"'.format(trait_value, trait_name))
        return trait_value

    def get_characteristic_multiplier(self, characteristic):
        trait_name = 'unnatural_{}'.format(characteristic)
        trait_value = self.get_trait(trait_name)
        if trait_value is not None:
            multiplier = trait_value
        else:
            multiplier = DEFAULT_CHARACTERISTIC_MULTIPLIER
        return multiplier
