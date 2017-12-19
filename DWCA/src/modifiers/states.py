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
