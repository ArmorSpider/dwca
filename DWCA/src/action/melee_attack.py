from src.action.attack import Attack
from src.entities.char_stats import STAT_STR


class MeleeAttack(Attack):

    def is_melee(self):
        return True

    def calculate_flat_damage(self):
        flat_damage = Attack.calculate_flat_damage(self)
        str_bonus = self.attacker.get_characteristic_bonus(STAT_STR)
        flat_damage += str_bonus
        return flat_damage
