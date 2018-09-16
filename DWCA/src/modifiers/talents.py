from src.cli.message_queue import queue_message
from src.dwca_log.log import get_log
from src.entities.char_stats import STAT_INT, STAT_PER, STAT_WS, STAT_BS
from src.modifiers.modifier import Modifier


LOG = get_log(__name__)


class CrushingBlow(Modifier):

    name = 'crushing_blow'

    def modify_damage(self, attack, current_damage):
        if attack.is_melee():
            crushing_blow_damage = attack.get_characteristic_bonus(
                STAT_WS) / 2
            current_damage += crushing_blow_damage
            LOG.debug('+%s damage from CrushingBlow.', crushing_blow_damage)
        return current_damage


class MightyShot(Modifier):

    name = 'mighty_shot'

    def modify_damage(self, attack, current_damage):
        if attack.is_ranged():
            mighty_shot_damage = attack.get_characteristic_bonus(
                STAT_BS) / 2
            current_damage += mighty_shot_damage
            LOG.debug('+%s damage from MightyShot.', mighty_shot_damage)
        return current_damage


class FleshRender(Modifier):

    name = 'flesh_render'

    def modify_tearing_dice(self, attack, current_tearing_dice):
        if attack.is_melee() and attack.tearing is not None:
            LOG.debug('+1 tearing dice from FleshRender.')
            current_tearing_dice += 1
        return current_tearing_dice


class SlaughterTheSwarm(Modifier):

    name = 'slaughter_the_swarm'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.target.is_horde():
            int_mod = attack.get_characteristic_bonus(STAT_INT)
            per_mod = attack.get_characteristic_bonus(STAT_PER)
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


class SlayerOfDaemons(Modifier):

    name = 'slayer_of_daemons'

    def modify_damage(self, attack, current_damage):
        if attack.target.is_daemon() and attack.is_melee():
            LOG.debug('+2 damage from SlayerOfDaemons against daemons.')
            current_damage += 2
        return current_damage


class WarpConduit(Modifier):

    name = 'warp_conduit'

    def modify_psy_rating(self, attack, psy_rating):
        if attack.push is not None:
            psy_rating += 1
            LOG.debug('+1 Psy Rating from WarpConduit when pushing.')
        return psy_rating


class BerserkCharge(Modifier):

    name = 'berserk_charge'


class HardTarget(Modifier):

    name = 'hard_target'

    def modify_num_dice(self, attack, current_num_dice):
        if attack.charged is not None:
            queue_message(
                'HARD TARGET: BS attacks against %s have -40 until %s\'s next turn.' % (attack.attacker, attack.attacker))
        return current_num_dice


class Ambidextrous(Modifier):

    name = 'ambidextrous'


class TwoWeaponWielderMelee(Modifier):

    name = 'two_weapon_wielder_melee'


class BladeDancer(Modifier):

    name = 'blade_dancer'


class SwiftAttack(Modifier):

    name = 'swift_attack'


class LightningAttack(Modifier):

    name = 'lightning_attack'


class Sprint(Modifier):

    name = 'sprint'


class UnfetteredPsyker(Modifier):

    name = 'unfettered_psyker'
