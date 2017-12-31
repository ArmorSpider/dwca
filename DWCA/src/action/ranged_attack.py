from lazy.lazy import lazy

from definitions import FIREMODE, NUM_HITS
from src.action.attack import Attack
from src.dwca_log.log import get_log
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO
from src.errors import NoFiremodeError
from src.modifiers.qualities import Storm, Blast
from src.situational.weapon_jam import is_attack_auto_failed


LOG = get_log(__name__)


class RangedAttack(Attack):

    def __init__(self, weapon, attacker, target, firemode):
        Attack.__init__(self, weapon, attacker, target)
        self.firemode = firemode

    @property
    def rate_of_fire(self):
        firemode = self.weapon.get_rof(self.firemode)
        return firemode

    def is_successfull(self):
        success = Attack.is_successfull(self)
        auto_fail = is_attack_auto_failed(self)
        return success is True and auto_fail is False

    @property
    def _num_shots(self):
        LOG.info('Firemode is "%s".', self.firemode)
        num_shots = 1
        if self.firemode == SINGLE_SHOT:
            num_shots = 1
        elif self.firemode == SEMI_AUTO:
            num_shots += int(self.degrees_of_success / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)',
                      num_shots, self.degrees_of_success)
        elif self.firemode == FULL_AUTO:
            num_shots += int(self.degrees_of_success)
            LOG.debug('DoS hits: %s (%s DoS)',
                      num_shots, self.degrees_of_success)
        else:
            raise NoFiremodeError(
                '"%s" did not match any known firemode.' % self.firemode)
        self._update_metadata({FIREMODE: self.firemode})
        LOG.debug('Max hits: %s. RoF cap: %s', num_shots, self.rate_of_fire)
        num_shots = min(num_shots, self.rate_of_fire)
        num_shots = Storm.handle_storm(self, num_shots)
        return num_shots

    @lazy
    def num_hits(self):
        num_hits = self._num_shots
        num_hits = Blast.handle_blast(self, num_hits)
        if self.weapon.damage_type == 'X' and self.target.is_horde():
            LOG.info('+1 hit from damage type X against hordes.')
            num_hits += 1
        for modifier in self.modifer_iterator():
            num_hits = modifier.modify_num_hits(self, num_hits)
        self._update_metadata({NUM_HITS: num_hits})
        return num_hits
