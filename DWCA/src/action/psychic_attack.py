from lazy.lazy import lazy

from src.action.attack import Attack
from src.dwca_log.log import get_log


LOG = get_log(__name__)


class PsychicAttack(Attack):

    def is_successfull(self):
        success = Attack.is_successfull(self)
        auto_fail = 91 <= self.roll_result <= 100
        return success is True and auto_fail is False

    @lazy
    def degrees_of_success(self):
        base_dos = super(Attack, self).degrees_of_success
        unnatural_wp = self.unnatural_willpower
        if base_dos >= 0 and unnatural_wp is not None:
            base_dos += unnatural_wp
            LOG.info('+%s DoS from UnnaturalWillpower.', unnatural_wp)
        return base_dos
