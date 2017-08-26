from src.action.attack import Attack
from src.dwca_log.log import get_log
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO


LOG = get_log(__name__)


class RangedAttack(Attack):

    def __init__(self, weapon, attacker, target, firemode):
        Attack.__init__(self, weapon, attacker, target)
        self.firemode = firemode

    def _calulcate_dos_hits(self):
        dos = self.get_degrees_of_success()
        LOG.info('Firemode is "%s".', self.firemode)
        if self.firemode == SINGLE_SHOT:
            dos_hits = 0
        elif self.firemode == SEMI_AUTO:
            dos_hits = int(dos / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)', dos_hits, dos)
        elif self.firemode == FULL_AUTO:
            dos_hits = int(dos)
            LOG.debug('DoS hits: %s (%s DoS)', dos_hits, dos)
        return dos_hits

    def _calulcate_firemode_hits(self):
        num_hits = 1
        dos_hits = self._calulcate_dos_hits()
        num_hits += dos_hits
        rof = self.get_weapon().get_rof(self.firemode)
        LOG.debug('Max hits: %s. RoF cap: %s', num_hits, rof)
        num_hits = min(num_hits, rof)
        LOG.info('Firemode hits: %s.', num_hits)
        return num_hits

    def _calculate_num_hits(self):
        firemode_hits = self._calulcate_firemode_hits()
        num_hits = firemode_hits
        for modifier in self._offensive_modifiers():
            num_hits = modifier.modify_num_hits(self, num_hits)
        return firemode_hits
