from src.entities import TRAITS, TALENTS, QUALITIES


class Attack(object):

    def __init__(self, weapon, attacker=None):
        self.weapon = weapon
        self.attacker = attacker

    def get_weapon(self):
        return self.weapon

    def get_attacker(self):
        return self.attacker

    def get_attacker_stat(self, stat_name):
        attacker = self.get_attacker()
        stat = attacker.get_stat(stat_name)
        return stat

    def get_weapon_stat(self, stat_name):
        weapon = self.get_weapon()
        stat = weapon.get_stat(stat_name)
        return stat

    def get_weapon_qualities(self):
        return self.get_weapon_stat(QUALITIES)

    def get_attacker_traits(self):
        return self.get_attacker_stat(TRAITS)

    def get_attacker_talents(self):
        return self.get_attacker_stat(TALENTS)
