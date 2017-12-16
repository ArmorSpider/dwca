from lazy.lazy import lazy

from src.action.attack import Attack
from src.dwca_log.log import get_log
from src.entities import FLAT_DAMAGE
from src.entities.char_stats import STAT_STR


LOG = get_log(__name__)


class MeleeAttack(Attack):

    @lazy
    def flat_damage(self):
        flat_damage = super(MeleeAttack, self).flat_damage
        str_bonus = self.attacker.get_characteristic_bonus(STAT_STR)
        LOG.info('Added strength bonus (%s) to flat damage (%s).',
                 str_bonus, flat_damage)
        flat_damage += str_bonus
        self._update_metadata({FLAT_DAMAGE: flat_damage})
        return flat_damage

    @lazy
    def num_hits(self):
        num_hits = super(MeleeAttack, self).num_hits
        if self.target.is_horde():
            dos = self.get_degrees_of_success()
            dos_hits = int(dos / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)', dos_hits, dos)
            num_hits += dos_hits
        return num_hits
