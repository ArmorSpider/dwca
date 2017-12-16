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

    @property
    def rof(self):
        firemode = self.weapon.get_rof(self.firemode)
        return firemode

    def is_successfull(self):
        success = Attack.is_successfull(self)
        auto_fail = is_attack_auto_failed(self)
        return success is True and auto_fail is False

    @property
    def _dos_hits(self):
        LOG.info('Firemode is "%s".', self.firemode)
        if self.firemode == SINGLE_SHOT:
            dos_hits = 0
        elif self.firemode == SEMI_AUTO:
            dos_hits = int(self.degrees_of_success / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)',
                      dos_hits, self.degrees_of_success)
        elif self.firemode == FULL_AUTO:
            dos_hits = int(self.degrees_of_success)
            LOG.debug('DoS hits: %s (%s DoS)',
                      dos_hits, self.degrees_of_success)
        else:
            raise NoFiremodeError(
                '"%s" did not match any known firemode.' % self.firemode)
        return dos_hits

    @property
    def firemode_hits(self):
        rof_hits = 1
        rof_hits += self._dos_hits
        LOG.debug('Max hits: %s. RoF cap: %s', rof_hits, self.rof)
        firemode_hits = min(rof_hits, self.rof)
        Storm.handle_storm(self, firemode_hits)
        LOG.debug('Firemode hits: %s.', firemode_hits)
        return firemode_hits

    def _calculate_num_hits(self):
        num_hits = self.firemode_hits
        if self.weapon.damage_type == 'X' and self.target.is_horde():
            LOG.info('+1 hit from damage type X against hordes.')
            num_hits += 1
        for modifier in self._offensive_modifiers():
            num_hits = modifier.modify_num_hits(self, num_hits)
        return num_hits
