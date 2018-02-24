from lazy.lazy import lazy

from src.action.attack import Attack
from src.dwca_log.log import get_log
from src.entities import FLAT_DAMAGE, DICE
from src.entities.char_stats import STAT_STR, STAT_WS
from src.modifiers.states import Helpless


LOG = get_log(__name__)


class MeleeAttack(Attack):

    def is_successfull(self):
        if self.helpless is not None:
            LOG.debug('HELPLESS: Automatic success for WS attacks')
            return True
        else:
            return super(MeleeAttack, self).is_successfull()

    @property
    def degrees_of_success(self):
        if self.helpless is not None:
            ws_bonus = self.attacker.get_characteristic_bonus(STAT_WS)
            LOG.debug('HELPLESS: Automatic DoS equal to WS bonus (%s)', ws_bonus)
            return ws_bonus
        else:
            return super(MeleeAttack, self).degrees_of_success

    @lazy
    def flat_damage(self):
        flat_damage = super(MeleeAttack, self).flat_damage
        str_bonus = self.attacker.get_characteristic_bonus(STAT_STR)
        LOG.debug('Added strength bonus (%s) to flat damage (%s).',
                  str_bonus, flat_damage)
        flat_damage += str_bonus
        self.update_metadata({FLAT_DAMAGE: flat_damage})
        return flat_damage

    @lazy
    def num_hits(self):
        num_hits = super(MeleeAttack, self).num_hits
        if self.target.is_horde():
            dos = self.degrees_of_success
            dos_hits = int(dos / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)', dos_hits, dos)
            num_hits += dos_hits
        return num_hits

    @lazy
    def num_dice(self):
        num_dice = super(MeleeAttack, self).num_dice
        num_dice = Helpless.handle_helpless(self, num_dice)
        self.update_metadata({DICE: num_dice})
        return num_dice
