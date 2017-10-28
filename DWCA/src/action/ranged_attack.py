from src.action.attack import Attack
from src.dwca_log.log import get_log
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.errors import NoFiremodeError
from src.modifiers.qualities import Storm
from src.situational.weapon_jam import is_attack_auto_failed


LOG = get_log(__name__)


class RangedAttack(Attack):

    def __init__(self, weapon, attacker, target, firemode):
        Attack.__init__(self, weapon, attacker, target)
        self.firemode = firemode

    def is_successfull(self):
        success = Attack.is_successfull(self)
        auto_fail = is_attack_auto_failed(self)
        return success is True and auto_fail is False

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
        else:
            raise NoFiremodeError(
                '"%s" did not match any known firemode.' % self.firemode)
        return dos_hits

    def _calculate_firemode_hits(self):
        num_hits = 1
        dos_hits = self._calulcate_dos_hits()
        num_hits += dos_hits
        rof = self.get_weapon().get_rof(self.firemode)
        LOG.debug('Max hits: %s. RoF cap: %s', num_hits, rof)
        num_hits = min(num_hits, rof)
        if self.get_weapon().get_quality(Storm.name) is not None:
            num_hits += num_hits
            LOG.info('Double RoF hits from "storm" quality.')
        LOG.debug('Firemode hits: %s.', num_hits)
        return num_hits

    def _calculate_num_hits(self):
        num_hits = self._calculate_firemode_hits()
        if self.get_weapon().get_stat('damage_type') == 'X' and self.get_target().is_horde():
            LOG.info('+1 hit from damage type X against hordes.')
            num_hits += 1
        for modifier in self._offensive_modifiers():
            num_hits = modifier.modify_num_hits(self, num_hits)
        return num_hits
