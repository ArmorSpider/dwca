from definitions import WEAPONS, FORCE_FIELD
from src.action.melee_attack import MeleeAttack
from src.action.psychic_attack import PsychicAttack
from src.action.ranged_attack import RangedAttack
from src.dwca_log.log import get_log
from src.entities import ARMOR, CHARACTERISTICS, TRAITS, TALENTS, SPECIES,\
    SINGLE_SHOT, WOUNDS, SKILLS
from src.entities.char_stats import STAT_TGH
from src.entities.entity import Entity
from src.entities.libraries import read_character
from src.entities.species import is_alien_species
from src.hit_location import HITLOC_ALL, get_hit_location_name
from src.modifiers.qualities import Felling
from src.modifiers.traits import Daemonic
from src.situational.cover import get_cover_armor_for_hitloc
from src.situational.force_field import ForceField
from src.skills import get_skill_characteristic, BasicSkills, get_all_skills,\
    AdvancedSkills, get_advanced_skills
from src.util.rand_util import get_tens


LOG = get_log(__name__)
UNDEFINED_ARMOR_VALUE = 0
UNDEFINED_CHARACTERISTIC_VALUE = 0
DEFAULT_CHARACTERISTIC_MULTIPLIER = 1


def build_character(char_name):
    character_definition = read_character(char_name)
    character = Character(character_definition)
    return character


class Character(Entity):

    def mitigate_hit(self, attack, hit):
        attack.on_hit_effects()
        armor = attack.get_effective_armor(hit.hit_location)
        toughness = self.get_modded_toughness_bonus(attack)
        effective_damage = hit.calculate_effective_damage(
            armor, toughness)
        effective_damage = attack.on_damage_effects(effective_damage)
        LOG.info('%s was hit in %s for %s damage.', self,
                 hit.hit_location, effective_damage)
        return effective_damage

    def get_num_melee_attacks(self):
        num_attacks = 1
        if self.swift_attack is not None:
            num_attacks += 1
            if self.lightning_attack is not None:
                num_attacks += 1
        if self.multiple_arms is not None:
            num_attacks += 1
        LOG.info('%s can make %s melee attacks.', self, num_attacks)
        return num_attacks

    def get_num_ranged_attacks(self):
        num_attacks = 1
        LOG.info('%s can make %s ranged attacks.', self, num_attacks)
        return num_attacks

    def attack(self, weapon, target=None, firemode=SINGLE_SHOT):
        LOG.info('%s attacks %s with a(n) %s.', self, target, weapon)
        if weapon.is_melee():
            return self._melee_attack(weapon, target)
        elif weapon.is_psychic():
            return self._psychic_attack(weapon, target)
        else:
            return self._ranged_attack(weapon, target, firemode)

    @property
    def available_skills(self):
        available_skills = {}
        for skill in get_all_skills():
            available_skills[skill] = self._get_effective_skill_rating(skill)
        for skill in get_advanced_skills():
            if skill not in self.skills:
                available_skills.pop(skill, None)
        return available_skills

    def _get_effective_skill_rating(self, skill):
        characteristic_value = self.get_skill_characteristic(skill)
        trained_value = self.skills.get(skill)
        if trained_value is not None:
            effective_skill_rating = characteristic_value + trained_value
        else:
            effective_skill_rating = characteristic_value / 2
        return effective_skill_rating

    def get_skill_characteristic(self, skill):
        char_stat = get_skill_characteristic(skill)
        characteristic_value = self.get_characteristic(char_stat)
        return characteristic_value

    def _melee_attack(self, weapon, target=None):
        return MeleeAttack(weapon=weapon,
                           attacker=self,
                           target=target)

    def _ranged_attack(self, weapon, target=None, firemode=SINGLE_SHOT):
        return RangedAttack(weapon=weapon,
                            attacker=self,
                            target=target,
                            firemode=firemode)

    def _psychic_attack(self, weapon, target=None):
        return PsychicAttack(weapon=weapon,
                             attacker=self,
                             target=target)

    def get_armor(self, hit_location):
        hitloc_name = get_hit_location_name(hit_location)
        armor = self.armor.get(hitloc_name)
        if armor is None:
            armor = self.armor.get(HITLOC_ALL, UNDEFINED_ARMOR_VALUE)
        cover_armor = get_cover_armor_for_hitloc(hit_location)
        total_armor = armor + cover_armor
        return total_armor

    def get_characteristic(self, characteristic):
        char_stat = self.characteristics.get(
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

    def get_characteristic_multiplier(self, characteristic):
        trait_name = 'unnatural_{}'.format(characteristic)
        trait_value = self.traits.get(trait_name)
        if trait_value is not None:
            multiplier = trait_value
        else:
            multiplier = DEFAULT_CHARACTERISTIC_MULTIPLIER
        return multiplier

    @property
    def size_bonus(self):
        return self.size if self.size is not None else 0

    @property
    def force_field(self):
        force_field_definition = self.get_stat(FORCE_FIELD)
        if force_field_definition is None:
            return None
        else:
            return ForceField(force_field_definition)

    @property
    def weapons(self):
        return self.get_stat(WEAPONS, ['unarmed'])

    @property
    def species(self):
        return self.get_stat(SPECIES, 'NO_SPECIES')

    @property
    def traits(self):
        traits = self.get_stat(TRAITS, default={})
        return traits

    @property
    def skills(self):
        skills = self.get_stat(SKILLS, default={})
        return skills

    @property
    def talents(self):
        talents = self.get_stat(TALENTS, default={})
        return talents

    @property
    def wounds(self):
        wounds = self.get_stat(WOUNDS, default=0)
        return wounds

    @property
    def modifiers(self):
        modifiers = {}
        modifiers.update(self.traits)
        modifiers.update(self.talents)
        return modifiers

    @property
    def characteristics(self):
        return self.get_stat(CHARACTERISTICS, default={})

    @property
    def armor(self):
        return self.get_stat(ARMOR, default={})

    def is_alien(self):
        return is_alien_species(self.species)

    def is_daemon(self):
        return self.species == 'daemon'
