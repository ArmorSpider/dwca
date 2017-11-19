from definitions import WEAPONS, FORCE_FIELD
from src.action.melee_attack import MeleeAttack
from src.action.ranged_attack import RangedAttack
from src.dwca_log.log import get_log
from src.entities import ARMOR, CHARACTERISTICS, TRAITS, TALENTS, SPECIES,\
    SINGLE_SHOT
from src.entities.char_stats import STAT_TGH
from src.entities.entity import Entity
from src.entities.libraries import read_character
from src.entities.species import is_alien_species
from src.hit_location import HITLOC_ALL, get_hit_location_name
from src.modifiers.qualities import Felling, Toxic, DrainLife, Hellfire, Snare,\
    Flexible, WarpWeapon
from src.modifiers.talents import SwiftAttack, LightningAttack
from src.modifiers.traits import MultipleArms, Daemonic
from src.situational.cover import get_cover_armor_for_hitloc
from src.situational.force_field import ForceField
from src.util.rand_util import get_tens


LOG = get_log(__name__)
UNDEFINED_ARMOR_VALUE = 0
UNDEFINED_CHARACTERISTIC_VALUE = 0
DEFAULT_CHARACTERISTIC_MULTIPLIER = 1


def get_char(char_name):
    char_definition = read_character(char_name)
    char = Character(char_definition)
    return char


class Character(Entity):

    @property
    def force_field(self):
        force_field_definition = self.get_stat(FORCE_FIELD)
        if force_field_definition is None:
            return None
        else:
            return ForceField(force_field_definition)

    @property
    def weapons(self):
        return self.get_stat(WEAPONS, [])

    def mitigate_hit(self, attack, hit):
        self._on_hit(attack)
        armor = self.get_armor(hit.hit_location)
        armor = Hellfire.handle_hellfire_armor(attack, armor)
        armor = WarpWeapon.handle_warp_weapon(attack, armor)
        toughness = self.get_modded_toughness_bonus(attack)
        effective_damage = hit.calculate_effective_damage(
            armor, toughness)
        LOG.info('%s was hit in %s for %s damage.', self,
                 hit.hit_location, effective_damage)
        self._on_damage(attack, effective_damage)
        return effective_damage

    def _on_hit(self, attack):
        Snare.handle_snare(attack)
        Flexible.handle_flexible(attack)

    def _on_damage(self, attack, effective_damage):
        Toxic.handle_toxic(attack, effective_damage)
        DrainLife.handle_drain_life(attack, effective_damage)

    def get_num_melee_attacks(self):
        num_attacks = 1
        if self.get_talent(SwiftAttack.name) is not None:
            num_attacks += 1
        if self.get_talent(LightningAttack.name) is not None:
            num_attacks += 1
        if self.get_trait(MultipleArms.name) is not None:
            num_attacks += 1
        LOG.info('%s can make %s melee attacks.', self, num_attacks)
        return num_attacks

    def get_num_ranged_attacks(self):
        num_attacks = 1
        LOG.info('%s can make %s ranged attacks.', self, num_attacks)
        return num_attacks

    def attack(self, weapon, target=None, firemode=SINGLE_SHOT):
        if weapon.is_melee():
            return self._melee_attack(weapon, target)
        else:
            return self._ranged_attack(weapon, target, firemode)

    def _melee_attack(self, weapon, target=None):
        LOG.info('%s attacks %s with a(n) %s.', self, target, weapon)
        return MeleeAttack(weapon=weapon,
                           attacker=self,
                           target=target)

    def _ranged_attack(self, weapon, target=None, firemode=SINGLE_SHOT):
        LOG.info('%s attacks %s with a(n) %s.', self, target, weapon)
        return RangedAttack(weapon=weapon,
                            attacker=self,
                            target=target,
                            firemode=firemode)

    def _get_species(self):
        return self.get_stat(SPECIES, 'N/A')

    def is_alien(self):
        return is_alien_species(self._get_species())

    def get_armor(self, hit_location):
        armor_dict = self._get_armor_definition()
        hitloc_name = get_hit_location_name(hit_location)
        armor = armor_dict.get(hitloc_name)
        if armor is None:
            armor = armor_dict.get(HITLOC_ALL, UNDEFINED_ARMOR_VALUE)
        cover_armor = get_cover_armor_for_hitloc(hit_location)
        total_armor = armor + cover_armor
        return total_armor

    def _get_armor_definition(self):
        return self.get_stat(ARMOR, default={})

    def _get_characteristics(self):
        return self.get_stat(CHARACTERISTICS, default={})

    def get_characteristic(self, characteristic):
        char_stats = self._get_characteristics()
        char_stat = char_stats.get(
            characteristic, UNDEFINED_CHARACTERISTIC_VALUE)
        return char_stat

    def get_raw_characteristic_bonus(self, characteristic):
        characteristic_value = self.get_characteristic(characteristic)
        characteristic_bonus = get_tens(characteristic_value)
        return characteristic_bonus

    def get_modded_toughness_bonus(self, attack):
        raw_bonus = self.get_raw_characteristic_bonus(STAT_TGH)
        tgh_multiplier = self.get_characteristic_multiplier(STAT_TGH)
        tgh_multiplier = Felling.handle_felling(attack, tgh_multiplier)
        tgh_multiplier = Daemonic.handle_daemonic(attack, tgh_multiplier)
        final_bonus = raw_bonus * tgh_multiplier
        return final_bonus

    def get_characteristic_bonus(self, characteristic):
        characteristic_bonus = self.get_raw_characteristic_bonus(
            characteristic)
        characteristic_multiplier = self.get_characteristic_multiplier(
            characteristic)
        final_bonus = characteristic_bonus * characteristic_multiplier
        return final_bonus

    def get_talent(self, talent_name):
        talents = self.get_stat(TALENTS, default={})
        talent_value = talents.get(talent_name)
        LOG.log(5, 'Found value "%s" for talent "%s"',
                talent_value, talent_name)
        return talent_value

    def get_trait(self, trait_name, default=None):
        traits = self.get_stat(TRAITS, default={})
        trait_value = traits.get(trait_name, default)
        LOG.log(5, 'Found value "%s" for trait "%s"', trait_value, trait_name)
        return trait_value

    def get_characteristic_multiplier(self, characteristic):
        trait_name = 'unnatural_{}'.format(characteristic)
        trait_value = self.get_trait(trait_name)
        if trait_value is not None:
            multiplier = trait_value
        else:
            multiplier = DEFAULT_CHARACTERISTIC_MULTIPLIER
        return multiplier
