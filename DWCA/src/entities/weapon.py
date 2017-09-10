from definitions import CLASS, MELEE
from src.entities import QUALITIES, SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.entities.entity import Entity
from src.util.read_file import read_weapon


def get_weapon(weapon_name):
    weap_definition = read_weapon(weapon_name)
    weapon = Weapon(weap_definition)
    return weapon


class Weapon(Entity):

    def is_melee(self):
        weapon_class = self.get_stat(CLASS)
        return weapon_class.lower() == MELEE

    def get_quality(self, quality_name, default=None):
        qualities = self.get_stat(QUALITIES, default={})
        quality_value = qualities.get(quality_name, default)
        return quality_value

    def get_rof(self, firemode):
        rof = self.get_stat(firemode)
        return rof

    @property
    def firemodes(self):
        known_firemodes = [SINGLE_SHOT, SEMI_AUTO, FULL_AUTO]
        available_firemodes = {}
        for firemode in known_firemodes:
            rof = self.get_stat(firemode)
            if rof is not None:
                available_firemodes[firemode] = rof
        return available_firemodes
