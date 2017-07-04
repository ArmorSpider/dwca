from src.dwca_log.log import get_log
from src.entities import TRAITS, TALENTS, QUALITIES, DICE, PENETRATION, DAMAGE
from src.entities.action import Action


LOG = get_log(__name__)


class Attack(Action):

    def __init__(self, weapon, attacker=None):
        self.weapon = weapon
        self.attacker = attacker

    def get_weapon(self):
        return self.weapon

    def get_attacker(self):
        return self.attacker

    def calculate_num_dice(self):
        num_dice = self._get_weapon_stat(DICE)
        # TODO: Calculate modifiers!
        return num_dice

    def calculate_penetration(self):
        penetration = self._get_weapon_stat(PENETRATION)
        # TODO: Calculate modifiers!
        # razor sharp
        return penetration

    def calculate_flat_damage(self):
        flat_damage = self._get_weapon_stat(DAMAGE)
        # TODO: Calculate modifiers!
        # Str bonus if melee
        return flat_damage

    def _get_attacker_stat(self, stat_name):
        attacker = self.get_attacker()
        stat = attacker.get_stat(stat_name)
        return stat

    def _get_weapon_stat(self, stat_name):
        weapon = self.get_weapon()
        stat = weapon.get_stat(stat_name)
        return stat

    def get_weapon_qualities(self):
        return self._get_weapon_stat(QUALITIES)

    def get_attacker_traits(self):
        return self._get_attacker_stat(TRAITS)

    def get_attacker_talents(self):
        return self._get_attacker_stat(TALENTS)
