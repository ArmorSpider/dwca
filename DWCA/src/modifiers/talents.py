from src.modifiers.modifier import Modifier
from src.modifiers.qualities import Tearing


class CrushingBlow(Modifier):

    name = 'crushing_blow'

    def modify_damage(self, attack, current_damage):
        if attack.is_melee():
            current_damage += 2
        return current_damage


class MightyShot(Modifier):

    name = 'mighty_shot'

    def modify_damage(self, attack, current_damage):
        if attack.is_ranged():
            current_damage += 2
        return current_damage


class FleshRender(Modifier):

    name = 'flesh_render'

    def modify_tearing_dice(self, attack, current_tearing_dice):
        if attack.is_melee() and attack.get_weapon().get_quality(Tearing.name):
            return current_tearing_dice + 1


class DeathwatchTraining(Modifier):

    name = 'deathwatch_training'


class SwiftAttack(Modifier):

    name = 'swift_attack'


class LightningAttack(Modifier):

    name = 'lightning_attack'
