from src.action.attack import Attack
from src.dwca_log.log import get_log
from src.entities.char_stats import STAT_STR


LOG = get_log(__name__)


class MeleeAttack(Attack):

    def _calculate_flat_damage(self):
        flat_damage = Attack._calculate_flat_damage(self)
        str_bonus = self.attacker.get_characteristic_bonus(STAT_STR)
        flat_damage += str_bonus
        return flat_damage

    def _calculate_num_hits(self):
        num_hits = Attack._calculate_num_hits(self)
        if self.get_target().is_horde():
            dos = self.get_degrees_of_success()
            dos_hits = int(dos / 2)
            LOG.debug('DoS hits: %s (%s DoS/2)', dos_hits, dos)
            num_hits += dos_hits
        return num_hits
