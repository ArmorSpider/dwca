from src.cli.message_queue import queue_message
from src.dice import roll_damage_dice, roll_damage_die
from src.dwca_log.log import get_log
from src.entities.char_stats import STAT_TGH, STAT_STR
from src.modifiers.modifier import Modifier


LOG = get_log(__name__)


class PsychicScaling(Modifier):

    name = 'psychic_scaling'

    def modify_num_dice(self, attack, current_num_dice):
        return self.scale_with_pr(attack, current_num_dice)

    def modify_penetration(self, attack, current_penetration):
        return self.scale_with_pr(attack, current_penetration)

    def modify_damage(self, attack, current_damage):
        return self.scale_with_pr(attack, current_damage)

    def scale_with_pr(self, attack, current_value):
        if attack.effective_psy_rating is not None:
            current_value = current_value * attack.effective_psy_rating
        return current_value


class Balanced(Modifier):

    name = 'balanced'


class Unbalanced(Modifier):

    name = 'unbalanced'


class Unwieldy(Modifier):

    name = 'unwieldy'


class RazorSharp(Modifier):

    name = 'razor_sharp'

    def modify_penetration(self, attack, current_penetration):
        if attack.degrees_of_success >= 2:
            current_penetration += attack.weapon.penetration
            LOG.debug('Double penetration from RazorSharp.')
        return current_penetration


class OverHeats(Modifier):

    name = 'overheats'

    @staticmethod
    def handle_overheats(attack):
        if attack.overheats is not None:
            dice = attack.weapon.dice
            flat_damage = attack.weapon.flat_damage
            damage_string = '{}d10+{}'.format(dice, flat_damage)
            message_base = ('OVERHEATS: {weapon} overheats! {attacker} takes {damage_string} damage to random arm. '
                            'This weapon cannot be fired for one round.')
            message = message_base.format(weapon=attack.weapon,
                                          attacker=attack.attacker,
                                          damage_string=damage_string)
            queue_message(message)


class Reliable(Modifier):

    name = 'reliable'


class NeverJams(Modifier):

    name = 'never_jams'


class Tearing(Modifier):

    name = 'tearing'

    def modify_tearing_dice(self, attack, current_tearing_dice):
        current_tearing_dice += 1
        LOG.debug('+1 tearing dice from Tearing.')
        return current_tearing_dice


class Felling(Modifier):

    name = 'felling'

    @staticmethod
    def handle_felling(attack, tgh_multiplier):
        felling_value = attack.felling
        if felling_value is not None:
            tgh_multiplier = max(tgh_multiplier - felling_value, 1)
            LOG.debug('Toughness multiplier reduced by Felling(%s)',
                      felling_value)
        return tgh_multiplier


class Volatile(Modifier):

    name = 'volatile'


class DrainLife(Modifier):

    name = 'drain_life'

    def on_damage(self, attack, effective_damage):
        if attack.drain_life is not None \
                and effective_damage > 0:
            message = ('DRAIN_LIFE: Make an opposed WP Test. '
                       'Each DoS for %s deals 1d10 true damage to %s.')
            queue_message(message % (attack.attacker, attack.target))
        return effective_damage


class Proven(Modifier):

    name = 'proven'

    @staticmethod
    def handle_proven(attack, roll_results):
        proven_value = attack.proven
        if proven_value is not None:
            modified_results = [max(value, proven_value)
                                for value in roll_results]
            LOG.debug('Proved modified roll result to %s.', modified_results)
            return modified_results
        else:
            return roll_results


class Shocking(Modifier):

    name = 'shocking'

    def on_damage(self, attack, effective_damage):
        if effective_damage > 0:
            queue_message('SHOCKING: %s must make TGH test +10*(location AP) or be stunned for %s rounds.' %
                          (attack.target, int(effective_damage * 0.5)))
        return effective_damage


class Toxic(Modifier):

    name = 'toxic'

    def on_damage(self, attack, effective_damage):
        toxic_value = attack.toxic
        if toxic_value is not None and effective_damage > 0:
            penalty = 10 * toxic_value
            queue_message('TOXIC: %s should roll %s -%s or take 1d10 true damage.' %
                          (attack.target, STAT_TGH, penalty))


class TwinLinked(Modifier):

    name = 'twin_linked'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.degrees_of_success >= 2:
            LOG.debug('+1 hit from TwinLinked.')
            current_num_hits += 1
        return current_num_hits


class LivingAmmunition(Modifier):

    name = 'living_ammunition'


class Sanctified(Modifier):

    name = 'sanctified'


class ForceWeapon(Modifier):

    name = 'force_weapon'

    def modify_damage(self, attack, current_damage):
        psy_rating = attack.psy_rating
        if psy_rating is not None:
            current_damage += psy_rating
            LOG.info('+%s damage from ForceWeapon + PsyRating', psy_rating)
        return current_damage

    def modify_penetration(self, attack, current_penetration):
        psy_rating = attack.psy_rating
        if psy_rating is not None:
            current_penetration += psy_rating
            LOG.info('+%s penetration from ForceWeapon + PsyRating', psy_rating)
        return current_penetration


class Accurate(Modifier):

    name = 'accurate'

    def modify_damage(self, attack, current_damage):
        if attack.degrees_of_success >= 2:
            if attack.aimed is True:
                current_damage += roll_damage_die()
                LOG.info('+1d10 damage from Accurate with DoS >= 2')
                if attack.degrees_of_success >= 4:
                    current_damage += roll_damage_die()
                    LOG.info('+1d10 damage from Accurate with DoS >= 4')
        return current_damage


class Blast(Modifier):

    name = 'blast'

    @staticmethod
    def handle_blast(attack, num_hits):
        if attack.blast is not None and attack.target.is_horde():
            num_hits = num_hits * attack.blast
        return num_hits

    def on_hit(self, attack):
        queue_message('BLAST: Everyone within %sm of %s must dodge or take damage.' % (
            attack.blast, attack.target))


class PowerField(Modifier):

    name = 'power_field'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.target.is_horde():
            current_num_hits += 1
            LOG.debug('+1 hit from PowerField against hordes.')
        return current_num_hits


class Storm(Modifier):

    name = 'storm'

    @staticmethod
    def handle_storm(attack, rof_hits):
        if attack.storm is not None:
            rof_hits += rof_hits
            LOG.info('Double RoF hits from "storm" quality.')
        return rof_hits


class Snare(Modifier):

    name = 'snare'

    def on_hit(self, attack):
        if attack.snare is not None:
            queue_message('SNARE: %s must make AGI test or be immobilised.')


class DeadlySnare(Modifier):

    name = 'deadly_snare'

    def on_hit(self, attack):
        if attack.deadly_snare is not None:
            damage_roll_base = '{dice}d10+{flat_damage} Pen: {pen}'
            damage_roll = damage_roll_base.format(dice=attack.num_dice,
                                                  flat_damage=attack.flat_damage,
                                                  pen=attack.penetration)
            queue_message(
                'DEADLY_SNARE: %s must make AGI test or be immobilised.'
                'Take %s each turn until escape.' % (attack.target, damage_roll))


class Flexible(Modifier):

    name = 'flexible'

    def on_hit(self, attack):
        _ = attack
        queue_message('FLEXIBLE: Attack cannot be parried.')


class Hellfire(Modifier):

    name = 'hellfire'

    def modify_armor(self, attack, current_armor, hit_location):
        if attack.target.natural_armor is not None:
            LOG.info('Hellfire negates natural armor.')
            current_armor = 0
        return current_armor

    @staticmethod
    def handle_hellfire_magnitude_damage(attack, magnitude_damage):
        if attack.hellfire is not None and magnitude_damage > 0:
            LOG.info('+1 magnitude damage per hit from Hellfire.')
            magnitude_damage += 1
        return magnitude_damage


class WarpWeapon(Modifier):

    name = 'warp_weapon'

    def modify_armor(self, attack, current_armor, hit_location):
        LOG.info('WarpWeapon ignores mundane armor.')
        current_armor = 0
        return current_armor


class Devastating(Modifier):

    name = 'devastating'

    def on_hit(self, attack):
        queue_message('DEVASTATING: %s takes one cohesion damage.' %
                      attack.target)

    @staticmethod
    def handle_devastating(attack, magnitude_damage):
        devastating_value = attack.devastating
        if devastating_value is not None:
            LOG.info('+%s magnitude damage from Devastating.',
                     devastating_value)
            magnitude_damage += devastating_value
        return magnitude_damage


class Concussive(Modifier):

    name = 'concussive'

    def on_hit(self, attack):
        test_difficulty = -10 * attack.degrees_of_success
        queue_message('CONCUSSIVE: %s must make TGH test (%s) or be Stunned for 1 round.' %
                      (attack.target, test_difficulty))

    def on_damage(self, attack, effective_damage):
        str_bonus = attack.target.get_characteristic_bonus(STAT_STR)
        if effective_damage > str_bonus:
            queue_message('CONCUSSIVE: Damage was > STR bonus. (%s > %s). %s is knocked down.' % (
                effective_damage, str_bonus, attack.target))
        return effective_damage


class MultiplyStrength(Modifier):

    name = 'multiply_strength'

    def modify_damage(self, attack, current_damage):
        strength_multiplier = attack.multiply_strength
        raw_str_bonus = attack.attacker.get_raw_characteristic_bonus(STAT_STR)
        if strength_multiplier is not None:
            current_damage += (strength_multiplier * raw_str_bonus)
            LOG.info('Added extra strength multiplier. (%s * %s)',
                     strength_multiplier, raw_str_bonus)
        return current_damage


class Markerlight(Modifier):

    name = 'markerlight'

    def on_hit(self, attack):
        queue_message('MARKERLIGHT: +10 to all BS tests against %s. (Cumulative)' %
                      attack.target)
        queue_message(
            'MARKERLIGHT: %s can be targeted with seeker missiles (BS 80) for one round.' % attack.target)


class NonDamaging(Modifier):

    name = 'non_damaging'


class DamagePerDos(Modifier):

    name = 'damage_per_dos'

    def modify_damage(self, attack, current_damage):
        dos = attack.degrees_of_success
        damage_per_dos = attack.damage_per_dos
        bonus_damage = max(0, damage_per_dos * dos)
        LOG.info('+%s damage from DamagePerDos(%s)',
                 bonus_damage, damage_per_dos)
        current_damage += bonus_damage
        return current_damage


class PenetrationPerDos(Modifier):

    name = 'penetration_per_dos'

    def modify_penetration(self, attack, current_penetration):
        dos = attack.degrees_of_success
        penetration_per_dos = attack.penetration_per_dos
        bonus_penetration = max(0, penetration_per_dos * dos)
        LOG.info('+%s penetration from PenetrationPerDos(%s)',
                 bonus_penetration, penetration_per_dos)
        current_penetration += bonus_penetration
        return current_penetration


class Lance(Modifier):

    name = 'lance'

    def modify_penetration(self, attack, current_penetration):
        dos = attack.degrees_of_success
        bonus_penetration = max(0, 5 * dos)
        LOG.info('+%s penetration from Lance', bonus_penetration)
        current_penetration += bonus_penetration
        return current_penetration


class SkillBonus(Modifier):

    name = 'skill_bonus'
