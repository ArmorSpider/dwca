from src.entities.entity import Entity
from src.util.read_file import read_weapon


def get_weapon(weapon_name):
    weap_definition = read_weapon(weapon_name)
    weapon = Weapon(weap_definition)
    return weapon


class Weapon(Entity):

    def is_melee(self):
        weapon_class = self.get_stat('class')
        return weapon_class.lower() == 'melee'
