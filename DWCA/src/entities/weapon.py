from definitions import CLASS, MELEE, RANGED_CLASSES
from src.entities import QUALITIES, SINGLE_SHOT, SEMI_AUTO, FULL_AUTO,\
    DAMAGE_TYPE, FLAT_DAMAGE, PENETRATION, DICE, RANGE, PSYCHIC, STANDARD_ATTACK,\
    SWIFT_ATTACK, LIGHTNING_ATTACK
from src.entities.entity import Entity
from src.entities.libraries import read_weapon

# DEVTEST


def get_weapon(weapon_name):
    weap_definition = read_weapon(weapon_name)
    weapon = Weapon(weap_definition)
    return weapon


class Weapon(Entity):

    def is_psychic(self):
        return self.weapon_class.lower() == PSYCHIC

    def is_melee(self):
        return self.weapon_class.lower() == MELEE

    def is_ranged(self):
        return self.weapon_class.lower() in RANGED_CLASSES

    def get_rof(self, firemode):
        rate_of_fire = self.get_stat(firemode)
        return rate_of_fire

    @property
    def weapon_class(self):
        return self.get_stat(CLASS, MELEE)

    @property
    def range_options(self):
        base_range = self.base_range
        extreme_range = base_range * 3
        long_range = base_range * 2
        short_range = int(base_range * 0.5)
        point_blank = 2
        range_options = {extreme_range: -30,
                         long_range: -10,
                         base_range: 0,
                         short_range: 10,
                         point_blank: 30}
        return range_options

    @property
    def base_range(self):
        return self.get_stat(RANGE, 0)

    @property
    def flat_damage(self):
        return self.get_stat(FLAT_DAMAGE, 0)

    @property
    def penetration(self):
        return self.get_stat(PENETRATION, 0)

    @property
    def dice(self):
        return self.get_stat(DICE, 1)

    @property
    def firemodes(self):
        if self.is_ranged():
            known_firemodes = [SINGLE_SHOT, SEMI_AUTO, FULL_AUTO]
            available_firemodes = {}
            for firemode in known_firemodes:
                rate_of_fire = self.get_stat(firemode)
                if rate_of_fire is not None:
                    available_firemodes[firemode] = rate_of_fire
        elif self.is_melee():
            available_firemodes = {STANDARD_ATTACK: True,
                                   SWIFT_ATTACK: True,
                                   LIGHTNING_ATTACK: True}
            if self.unbalanced is not None or self.unwieldy is not None:
                available_firemodes.pop(LIGHTNING_ATTACK)
        return available_firemodes

    @property
    def qualities(self):
        qualities = self.get_stat(QUALITIES, default={})
        return qualities

    @property
    def modifiers(self):
        return self.qualities

    @property
    def damage_type(self):
        return self.get_stat(DAMAGE_TYPE, None)
