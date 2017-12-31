import math

from src.modifiers.modifier import Modifier
from src.situational.cover import is_hitloc_eligible_for_cover


class Charged(Modifier):

    name = 'charged'


class Aimed(Modifier):

    name = 'aimed'


class Cover(Modifier):

    name = 'cover'

    def modify_armor(self, attack, current_armor, hit_location):
        if is_hitloc_eligible_for_cover(hit_location):
            current_armor = attack.cover
        return current_armor


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
