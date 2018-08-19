import math

from src.modifiers.modifier import Modifier
from src.situational.cover import is_hitloc_eligible_for_cover


class TrueDamage(Modifier):

    name = 'true_damage'


class IgnoreArmor(Modifier):

    name = 'ignore_armor'


class IgnoreToughness(Modifier):

    name = 'ignore_toughness'


class BonusArmor(Modifier):

    name = 'bonus_armor'

    def modify_armor(self, attack, current_armor, hit_location):
        if attack.bonus_armor is not None:
            current_armor += attack.bonus_armor
        return current_armor


class BonusDamage(Modifier):

    name = 'bonus_damage'

    def modify_damage(self, attack, current_damage):
        if attack.bonus_damage is not None:
            current_damage += attack.bonus_damage
        return current_damage


class BonusPenetration(Modifier):

    name = 'bonus_penetration'

    def modify_penetration(self, attack, current_penetration):
        if attack.bonus_penetration is not None:
            current_penetration += attack.bonus_penetration
        return current_penetration


class ReducePenetration(Modifier):

    name = 'reduce_penetration'

    def modify_penetration(self, attack, current_penetration):
        if attack.reduce_penetration is not None:
            current_penetration -= attack.reduce_penetration
            current_penetration = max(current_penetration, 0)
        return current_penetration


class ReduceDamage(Modifier):

    name = 'reduce_damage'

    def on_damage(self, attack, effective_damage):
        if attack.reduce_damage is not None:
            effective_damage -= attack.reduce_damage
            effective_damage = max(effective_damage, 0)
        return effective_damage


class Charged(Modifier):

    name = 'charged'


class Aimed(Modifier):

    name = 'aimed'


class Cover(Modifier):

    name = 'cover'

    def modify_armor(self, attack, current_armor, hit_location):
        if is_hitloc_eligible_for_cover(hit_location):
            current_armor += attack.cover
        return current_armor


class Helpless(Modifier):

    name = 'helpless'

    @staticmethod
    def handle_helpless(attack, current_num_dice):
        if attack.helpless is not None:
            current_num_dice *= 2
        return current_num_dice


class Fettered(Modifier):

    name = 'fettered'

    def modify_psy_rating(self, attack, psy_rating):
        if psy_rating > 0:
            base_psy_rating = attack.psy_rating
            fettered_penalty = int(
                base_psy_rating - (math.ceil(base_psy_rating * 0.5)))
            psy_rating -= fettered_penalty
        return psy_rating


class Unfettered(Modifier):

    name = 'unfettered'


class Push(Modifier):

    name = 'push'

    def modify_psy_rating(self, attack, psy_rating):
        if psy_rating > 0:
            psy_rating += 3
        return psy_rating


class BonusPR(Modifier):

    name = 'bonus_pr'

    def modify_psy_rating(self, attack, psy_rating):
        bonus_pr = attack.bonus_pr
        psy_rating += bonus_pr
        return psy_rating
