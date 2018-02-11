from lazy.lazy import lazy

from definitions import FIREMODE, NUM_HITS
from src.action.attack import Attack
from src.dwca_log.log import get_log
from src.entities import FLAT_DAMAGE, SWIFT_ATTACK, LIGHTNING_ATTACK
from src.entities.char_stats import STAT_STR, STAT_WS


LOG = get_log(__name__)


class MeleeAttack(Attack):

    def __init__(self, weapon, attacker, target, firemode):
        super(MeleeAttack, self).__init__(weapon, attacker, target)
        self.firemode = firemode
        self.update_metadata({FIREMODE: self.firemode})

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
        num_hits += self._dos_hits
        num_hits += self._horde_dos_hits
        self.update_metadata({NUM_HITS: num_hits})
        return num_hits

    @property
    def _dos_hits(self):
        dos_hits = 0
        dos = self.degrees_of_success
        if self.firemode == SWIFT_ATTACK:
            dos_hits += int(dos - 1 / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)',
                      dos_hits, dos)
        elif self.firemode == LIGHTNING_ATTACK:
            dos_hits += int(dos - 1)
            LOG.debug('DoS hits: %s (%s DoS)',
                      dos_hits, dos)
        ws_bonus = self.attacker.get_characteristic_bonus(STAT_WS)
        dos_hits = min(ws_bonus, dos_hits)
        return dos_hits

    @property
    def _horde_dos_hits(self):
        horde_dos_hits = 0
        if self.target.is_horde():
            horde_dos_hits += int(self.degrees_of_success / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)',
                      horde_dos_hits, self.degrees_of_success)
        return horde_dos_hits
