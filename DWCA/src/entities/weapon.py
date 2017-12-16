from definitions import CLASS, MELEE
from src.entities import QUALITIES, SINGLE_SHOT, SEMI_AUTO, FULL_AUTO,\
    DAMAGE_TYPE, FLAT_DAMAGE, PENETRATION, DICE
from src.entities.entity import Entity
from src.entities.libraries import read_weapon


def get_weapon(weapon_name):
    weap_definition = read_weapon(weapon_name)
    weapon = Weapon(weap_definition)
    return weapon


class Weapon(Entity):

    def is_melee(self):
        weapon_class = self.get_stat(CLASS, 'Melee')
        return weapon_class.lower() == MELEE

    def get_rof(self, firemode):
        rate_of_fire = self.get_stat(firemode)
        return rate_of_fire

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
        known_firemodes = [SINGLE_SHOT, SEMI_AUTO, FULL_AUTO]
        available_firemodes = {}
        for firemode in known_firemodes:
            rate_of_fire = self.get_stat(firemode)
            if rate_of_fire is not None:
                available_firemodes[firemode] = rate_of_fire
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
