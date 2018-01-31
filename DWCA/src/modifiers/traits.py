from src.dwca_log.log import get_log
from src.modifiers.modifier import Modifier


LOG = get_log(__name__)


class Horde(Modifier):

    name = 'horde'


class Overwhelming(Modifier):

    name = 'overwhelming'

    def modify_num_dice(self, attack, current_num_dice):
        attacker = attack.attacker
        if attacker.is_horde():
            if attacker.magnitude >= 20:
                LOG.debug('+1d10 from Overwhelming.')
                current_num_dice += 1
        return current_num_dice


class PsyRating(Modifier):

    name = 'psy_rating'


class FireDrill(Modifier):

    name = 'fire_drill'


class NaturalArmor(Modifier):

    name = 'natural_armor'


class TouchedByTheFates(Modifier):

    name = 'touched_by_the_fates'


class MultipleArms(Modifier):

    name = 'multiple_arms'


class Daemonic(Modifier):

    name = 'daemonic'

    @staticmethod
    def handle_daemonic(attack, tgh_multiplier):
        daemonic_value = attack.target.daemonic
        bypass_daemonic = any([attack.sanctified,
                               attack.force_weapon,
                               attack.daemonic])
        if daemonic_value is not None and bypass_daemonic is False:
            tgh_multiplier += 1
            LOG.debug('+1 TGH multiplier from Daemonic.')
        return tgh_multiplier


class BrutalCharge(Modifier):

    name = 'brutal_charge'

    def modify_damage(self, attack, current_damage):
        if attack.attacker.is_horde() is False and attack.charged is not None:
            LOG.info('+3 damage from BrutalCharge')
            current_damage += 3
        return current_damage

    def modify_num_dice(self, attack, current_num_dice):
        if attack.attacker.is_horde() is True and attack.charged is not None:
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


class UnnaturalWillpower(Modifier):

    name = 'unnatural_willpower'

    def modify_psy_rating(self, attack, psy_rating):
        psy_rating += attack.unnatural_willpower
        return psy_rating


class Size(Modifier):

    name = 'size'
