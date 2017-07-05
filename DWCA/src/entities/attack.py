from src.dwca_log.log import get_log
from src.entities import TRAITS, TALENTS, QUALITIES, DICE, PENETRATION, DAMAGE
from src.entities.action import Action


LOG = get_log(__name__)


class Attack(Action):

    def __init__(self, weapon, attacker, target):
        self.weapon = weapon
        self.attacker = attacker
        self.target = target

    def get_weapon(self):
        return self.weapon

    def get_attacker(self):
        return self.attacker

    def get_target(self):
        return self.target

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

    def _get_target_stat(self, stat_name):
        return self._get_entity_stat(self.get_target(), stat_name)

    def _get_attacker_stat(self, stat_name):
        return self._get_entity_stat(self.get_attacker(), stat_name)

    def _get_weapon_stat(self, stat_name):
        return self._get_entity_stat(self.get_weapon(), stat_name)

    def _get_entity_stat(self, entity, stat_name):
        stat = entity.get_stat(stat_name)
        return stat

    def get_defensive_modifiers(self):
        modifiers = {}
        modifiers.update(self.get_target_traits())
        modifiers.update(self.get_target_talents())
        return modifiers

    def get_offensive_modifiers(self):
        modifiers = {}
        modifiers.update(self.get_weapon_qualities())
        modifiers.update(self.get_attacker_traits())
        modifiers.update(self.get_attacker_talents())
        return modifiers

    def get_weapon_qualities(self):
        return self._get_weapon_stat(QUALITIES)

    def get_attacker_traits(self):
        return self._get_attacker_stat(TRAITS)

    def get_attacker_talents(self):
        return self._get_attacker_stat(TALENTS)

    def get_target_traits(self):
        return self._get_target_stat(TRAITS)

    def get_target_talents(self):
        return self._get_target_stat(TALENTS)
