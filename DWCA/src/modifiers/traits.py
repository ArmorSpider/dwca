from src.dwca_log.log import get_log
from src.modifiers.modifier import Modifier
from src.situational.state_manager import StateManager, has_charged


LOG = get_log(__name__)


class Horde(Modifier):

    name = 'horde'

    def modify_num_dice(self, attack, current_num_dice):
        attacker = attack.get_attacker()
        if attacker.is_horde():
            magnitude = attacker.get_magnitude()
            if magnitude >= 10:
                LOG.debug('+1d10 from Horde with Magnitude >= 10.')
                current_num_dice += 1
            if magnitude >= 20:
                LOG.debug('+1d10 from Horde with Magnitude >= 20.')
                current_num_dice += 1
        return current_num_dice


class Overwhelming(Modifier):

    name = 'overwhelming'

    def modify_num_dice(self, attack, current_num_dice):
        attacker = attack.get_attacker()
        if attacker.is_horde():
            if attacker.get_magnitude() >= 20:
                LOG.debug('+1d10 from Overwhelming.')
                current_num_dice += 1
        return current_num_dice


class FireDrill(Modifier):

    name = 'fire_drill'


class NaturalArmor(Modifier):

    name = 'natural_armor'


class TouchedByTheFates(Modifier):

    name = 'touched_by_the_fates'


class MultipleArms(Modifier):

    name = 'multiple_arms'


class BrutalCharge(Modifier):

    name = 'brutal_charge'

    def modify_damage(self, attack, current_damage):
        if attack.attacker.is_horde() is False and has_charged() is True:
            LOG.info('+3 damage from BrutalCharge')
            current_damage += 3
        return current_damage

    def modify_num_dice(self, attack, current_num_dice):
        if attack.attacker.is_horde() is True and has_charged() is True:
            LOG.info('+1 dice from BrutalCharge for hordes.')
            current_num_dice += 1
        return current_num_dice


class PowerArmour(Modifier):

    name = 'power_armour'

    def modify_damage(self, attack, current_damage):
        if attack.is_melee():
            LOG.debug('Added 2 flat damage from Power Armour strength bonus.')
            current_damage += 2
        return current_damage