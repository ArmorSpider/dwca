from src.entities import CHARACTERISTICS
from src.entities.char_stats import ALL_CHARACTERISTICS
from src.skills import get_skill_characteristic
from src.util.rand_util import get_tens

UNDEFINED_CHARACTERISTIC_VALUE = 0
DEFAULT_CHARACTERISTIC_MULTIPLIER = 1


class Characteristics(object):

    def get_skill_characteristic(self, skill):
        char_stat = get_skill_characteristic(skill)
        characteristic_value = self.get_characteristic(char_stat)
        return characteristic_value

    def get_characteristic(self, characteristic):
        char_base = self.get_raw_characteristic(characteristic)
        char_flat_bonus = self.get_flat_characteristic_value(characteristic)
        char_total = char_base + char_flat_bonus
        return char_total

    def get_raw_characteristic(self, characteristic):
        char_stat = self.characteristics.get(
            characteristic, UNDEFINED_CHARACTERISTIC_VALUE)
        return char_stat

    def get_raw_characteristic_bonus(self, characteristic):
        characteristic_value = self.get_raw_characteristic(characteristic)
        characteristic_bonus = get_tens(characteristic_value)
        return characteristic_bonus

    def get_flat_characteristic_bonus(self, characteristic):
        flat_value = self.get_flat_characteristic_value(characteristic)
        flat_bonus = get_tens(flat_value)
        return flat_bonus

    def get_flat_characteristic_value(self, characteristic):
        key = '{}_bonus'.format(characteristic)
        value = self.characteristics.get(key, 0)
        return value

    def get_natural_bonus(self, characteristic):
        base_bonus = self.get_raw_characteristic_bonus(characteristic)
        flat_bonus = self.get_flat_characteristic_bonus(characteristic)
        natural_bonus = base_bonus + flat_bonus
        return natural_bonus

    def get_characteristic_bonus(self, characteristic):
        characteristic_bonus = self.get_raw_characteristic_bonus(
            characteristic)
        unnatural_bonus = self.get_unnatural_characteristic(
            characteristic)
        flat_bonus = self.get_flat_characteristic_bonus(characteristic)
        final_bonus = characteristic_bonus + unnatural_bonus + flat_bonus
        return final_bonus

    def get_characteristic_multiplier(self, characteristic):
        trait_value = self.get_unnatural_characteristic(characteristic)
        if trait_value is not None:
            multiplier = trait_value
        else:
            multiplier = DEFAULT_CHARACTERISTIC_MULTIPLIER
        return multiplier

    def get_unnatural_characteristic(self, characteristic):
        trait_name = 'unnatural_{}'.format(characteristic)
        trait_value = self.modifiers.get(trait_name, 0)
        return trait_value

    @property
    def characteristics(self):
        return self.get_stat(CHARACTERISTICS, default={})

    @property
    def effective_characteristics(self):
        effective_chars = {}
        for characteristic in ALL_CHARACTERISTICS:
            effective_char = self.get_characteristic(characteristic)
            effective_chars[characteristic] = effective_char
        return effective_chars

    @property
    def modifiers(self):
        return super(Characteristics, self).modifiers

    def get_stat(self, stat_name, default=None):
        return super(Characteristics, self).get_stat(stat_name, default)
