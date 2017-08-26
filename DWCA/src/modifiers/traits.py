from src.dwca_log.log import get_log
from src.modifiers.modifier import Modifier


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


class TouchedByTheFates(Modifier):

    name = 'touched_by_the_fates'


class MultipleArms(Modifier):

    name = 'multiple_arms'
