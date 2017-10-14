from src.dwca_log.log import get_log
from src.entities import PENETRATION, DICE, DAMAGE
from src.entities.char_stats import STAT_TGH
from src.message_queue import queue_message
from src.modifiers.modifier import Modifier
from src.modifiers.traits import NaturalArmor
from src.state_manager import StateManager


LOG = get_log(__name__)


class RazorSharp(Modifier):

    name = 'razor_sharp'

    def modify_penetration(self, attack, current_pen):
        if attack.get_degrees_of_success() >= 2:
            weapons_penetration = attack.get_weapon_stat(PENETRATION)
            current_pen += weapons_penetration
            LOG.debug('Double penetration from RazorSharp.')
            return current_pen
        else:
            return current_pen


class Tearing(Modifier):

    name = 'tearing'

    def modify_tearing_dice(self, attack, current_tearing_dice):
        LOG.debug('+1 tearing dice from Tearing.')
        return current_tearing_dice + 1


class Felling(Modifier):

    name = 'felling'


class Volatile(Modifier):

    name = 'volatile'


class DrainLife(Modifier):

    name = 'drain_life'

    @staticmethod
    def handle_drain_life(attack, effective_damage):
        if attack.weapon.get_quality(DrainLife.name) is not None \
                and effective_damage > 0:
            message = ('DRAIN_FILE: Make an opposed WP Test. '
                       'Each DoS for %s deals 1d10 true damage to %s.')
            queue_message(message % (attack.attacker, attack.target))


class Proven(Modifier):

    name = 'proven'

    @staticmethod
    def handle_proven(attack, roll_results):
        proven_value = attack.weapon.get_quality(Proven.name)
        if proven_value is not None:
            modified_results = [max(value, proven_value)
                                for value in roll_results]
            LOG.debug('Proved modified roll result to %s.', modified_results)
            return modified_results
        else:
            return roll_results


class Toxic(Modifier):

    name = 'toxic'

    @staticmethod
    def handle_toxic(attack, effective_damage):
        toxic_value = attack.weapon.get_quality(Toxic.name)
        if toxic_value is None:
            toxic_value = attack.get_attacker().get_trait(Toxic.name)
        if toxic_value is not None and effective_damage > 0:
            penalty = 5 * effective_damage
            queue_message('TOXIC: %s should roll %s -%s or take %s true damage.' %
                          (attack.get_target(), STAT_TGH, penalty, toxic_value))


class TwinLinked(Modifier):

    name = 'twin_linked'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.get_degrees_of_success() >= 2:
            LOG.debug('+1 hit from TwinLinked.')
            current_num_hits += 1
        return current_num_hits


class Accurate(Modifier):

    name = 'accurate'

    def modify_num_dice(self, attack, current_num_dice):
        if attack.get_degrees_of_success() >= 2:
            if StateManager.aimed is True:
                current_num_dice += 1
                LOG.info('+1d10 from Accurate with DoS >= 2')
                if attack.get_degrees_of_success() >= 4:
                    current_num_dice += 1
                    LOG.info('+1d10 from Accurate with DoS >= 4')
        return current_num_dice


class Blast(Modifier):

    name = 'blast'

    def modify_num_hits(self, attack, current_num_hits):
        blast_value = attack.get_weapon().get_quality(self.name)
        queue_message('BLAST: Everyone within %sm of %s must dodge or take damage.' % (
            blast_value, attack.get_target()))
        if attack.get_target().is_horde():
            bonus_hits = max(1, blast_value - 1)
            current_num_hits += bonus_hits
        return current_num_hits


class PowerField(Modifier):

    name = 'power_field'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.get_target().is_horde():
            current_num_hits += 1
            LOG.debug('+1 hit from PowerField against hordes.')
        return current_num_hits


class Storm(Modifier):

    name = 'storm'


class Snare(Modifier):

    name = 'snare'

    @staticmethod
    def handle_snare(attack):
        if attack.weapon.get_quality(Snare.name):
            queue_message('SNARE: %s must make AGI test or be immobilised.')


class DeadlySnare(Modifier):

    name = 'deadly_snare'

    @staticmethod
    def handle_deadly_snare(attack):
        if attack.weapon.get_quality(Snare.name):
            damage_roll_base = '{dice}d10+{flat_damage} Pen: {pen}'
            damage_roll = damage_roll_base.format(dice=attack.get_weapon_stat(DICE, 1),
                                                  flat_damage=attack.get_weapon_stat(
                                                      DAMAGE, 0),
                                                  pen=attack.get_weapon_stat(PENETRATION, 0))
            queue_message(
                'DEADLY_SNARE: %s must make AGI test or be immobilised.'
                'Take %s each turn until escape.' % damage_roll)


class Flexible(Modifier):

    name = 'flexible'

    @staticmethod
    def handle_flexible(attack):
        if attack.weapon.get_quality(Flexible.name):
            queue_message('FLEXIBLE: Attack cannot be parried.')


class Hellfire(Modifier):

    name = 'hellfire'

    @staticmethod
    def handle_hellfire_armor(attack, armor):
        if attack.weapon.get_quality(Hellfire.name) and attack.target.get_trait(NaturalArmor.name):
            LOG.info('Hellfire negates natural armor.')
            armor = 0
        return armor

    @staticmethod
    def handle_hellfire_magnitude_damage(attack, magnitude_damage):
        if attack.weapon.get_quality(Hellfire.name):
            LOG.info('+1 magnitude damage per hit from Hellfire.')
            magnitude_damage += 1
        return magnitude_damage


class Devastating(Modifier):

    name = 'devastating'

    @staticmethod
    def handle_devastating(attack, magnitude_damage):
        devastating_value = attack.get_weapon().get_quality(Devastating.name)
        if devastating_value is not None:
            LOG.info('+%s magnitude damage from Devastating.',
                     devastating_value)
            magnitude_damage += devastating_value
        return magnitude_damage


class DamagePerDos(Modifier):

    name = 'damage_per_dos'

    def modify_damage(self, attack, current_damage):
        dos = attack.get_degrees_of_success()
        damage_per_dos = attack.weapon.get_quality(DamagePerDos.name)
        bonus_damage = max(0, damage_per_dos * dos)
        LOG.info('+%s damage from DamagePerDos(%s)',
                 bonus_damage, damage_per_dos)
        current_damage += bonus_damage
        return current_damage
