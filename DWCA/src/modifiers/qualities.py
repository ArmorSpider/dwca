from src.entities import PENETRATION
from src.modifiers.modifier import Modifier


class RazorSharp(Modifier):

    name = 'razor_sharp'

    def modify_penetration(self, attack, current_pen):
        if attack.get_degrees_of_success() >= 2:
            weapons_penetration = attack.get_weapon_stat(PENETRATION)
            current_pen += weapons_penetration
            return current_pen


class Tearing(Modifier):

    name = 'tearing'

    def modify_tearing_dice(self, attack, current_tearing_dice):
        return current_tearing_dice + 1
