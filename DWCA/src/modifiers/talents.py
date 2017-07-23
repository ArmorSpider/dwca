from src.modifiers.modifier import Modifier


class CrushingBlow(Modifier):

    def __init__(self):
        self.modifier_name = 'crushing_blow'

    def modify_damage(self, attack, current_damage):
        if attack.is_melee():
            current_damage += 2
        return current_damage
