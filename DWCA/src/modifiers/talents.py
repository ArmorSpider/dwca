from src.dwca_log.log import get_log
from src.entities.char_stats import STAT_INT, STAT_PER
from src.modifiers.modifier import Modifier
from src.modifiers.qualities import Tearing


LOG = get_log(__name__)


class CrushingBlow(Modifier):

    name = 'crushing_blow'

    def modify_damage(self, attack, current_damage):
        if attack.is_melee():
            current_damage += 2
            LOG.debug('+2 damage from CrushingBlow.')
        return current_damage


class MightyShot(Modifier):

    name = 'mighty_shot'

    def modify_damage(self, attack, current_damage):
        if attack.is_ranged():
            current_damage += 2
            LOG.debug('+2 damage from MightyShot.')
        return current_damage


class FleshRender(Modifier):

    name = 'flesh_render'

    def modify_tearing_dice(self, attack, current_tearing_dice):
        if attack.is_melee() and attack.get_weapon().get_quality(Tearing.name):
            LOG.debug('+1 tearing dice from FleshRender.')
            return current_tearing_dice + 1


class SlaughterTheSwarm(Modifier):

    name = 'slaughter_the_swarm'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.target.is_horde():
            attacker = attack.attacker
            int_mod = attacker.get_characteristic_bonus(STAT_INT)
            per_mod = attacker.get_characteristic_bonus(STAT_PER)
            extra_hits = max(int_mod, per_mod)
            LOG.info('+%s hits from SlaughterTheSwarm.', extra_hits)
            current_num_hits += extra_hits
        return current_num_hits


class DeathwatchTraining(Modifier):

    name = 'deathwatch_training'


class HunterOfAliens(Modifier):

    name = 'hunter_of_aliens'

    def modify_damage(self, attack, current_damage):
        if attack.target.is_alien() and attack.is_melee():
            LOG.debug('+2 damage from HunterOfAliens against aliens.')
            current_damage += 2
        return current_damage


class SwiftAttack(Modifier):

    name = 'swift_attack'


class LightningAttack(Modifier):

    name = 'lightning_attack'
