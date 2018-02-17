from definitions import WEAPONS, FORCE_FIELD
from src.action.melee_attack import MeleeAttack
from src.action.psychic_attack import PsychicAttack
from src.action.ranged_attack import RangedAttack
from src.dwca_log.log import get_log
from src.entities import ARMOR, CHARACTERISTICS, TRAITS, TALENTS, SPECIES,\
    SINGLE_SHOT, WOUNDS, SKILLS, HALF_MOVE, CHARGE_MOVE, RUN_MOVE, FULL_MOVE,\
    STANDARD_ATTACK
from src.entities.char_stats import STAT_TGH, STAT_AGI
from src.entities.entity import Entity
from src.entities.libraries import read_character, get_character_library
from src.entities.species import is_alien_species
from src.hit_location import HITLOC_ALL, get_hit_location_name
from src.modifiers.qualities import Felling
from src.modifiers.traits import Daemonic
from src.situational.cover import get_cover_armor_for_hitloc
from src.situational.force_field import ForceField
from src.skills import get_skill_characteristic, get_all_skills
from src.util.rand_util import get_tens
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)
UNDEFINED_ARMOR_VALUE = 0
UNDEFINED_LOCATIONAL_TOUGHNESS_VALUE = 0
UNDEFINED_CHARACTERISTIC_VALUE = 0
DEFAULT_CHARACTERISTIC_MULTIPLIER = 1


def choose_character():
    available_characters = get_character_library().keys()
    character_name = try_user_choose_from_list(available_characters)
    return character_name


def build_character(char_name):
    character_definition = read_character(char_name)
    character = Character(character_definition)
    return character


class Character(Entity):

    @property
    def num_melee_attacks(self):
        num_attacks = 1
        LOG.info('%s can make %s melee attacks.', self, num_attacks)
        return num_attacks

    @property
    def num_ranged_attacks(self):
        num_attacks = 1
        LOG.info('%s can make %s ranged attacks.', self, num_attacks)
        return num_attacks

    def attack(self, weapon, target=None, firemode=SINGLE_SHOT):
        LOG.debug('%s attacks %s with a(n) %s.', self, target, weapon)
        if weapon.is_melee():
            return self._melee_attack(weapon, target, firemode)
        elif weapon.is_psychic():
            return self._psychic_attack(weapon, target)
        else:
            return self._ranged_attack(weapon, target, firemode)

    @property
    def available_skills(self):
        available_skills = {}
        for skill in get_all_skills():
            available_skills[skill] = self._get_effective_skill_rating(skill)
        return available_skills

    def _get_effective_skill_rating(self, skill):
        characteristic_value = self.get_skill_characteristic(skill)
        trained_value = self.skills.get(skill)
        if trained_value is not None:
            effective_skill_rating = characteristic_value + trained_value
        else:
            effective_skill_rating = characteristic_value - 20
        return effective_skill_rating

    def get_skill_characteristic(self, skill):
        char_stat = get_skill_characteristic(skill)
        characteristic_value = self.get_characteristic(char_stat)
        return characteristic_value

    def _melee_attack(self, weapon, target=None, firemode=STANDARD_ATTACK):
        return MeleeAttack(weapon=weapon,
                           attacker=self,
                           target=target,
                           firemode=firemode)

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

    def get_locational_toughness(self, hit_location):
        hitloc_name = get_hit_location_name(hit_location)
        toughness = self.toughness.get(hitloc_name)
        if toughness is None:
            toughness = self.toughness.get(
                HITLOC_ALL, UNDEFINED_LOCATIONAL_TOUGHNESS_VALUE)
        return toughness

    def get_characteristic(self, characteristic):
        char_stat = self.characteristics.get(
            characteristic, UNDEFINED_CHARACTERISTIC_VALUE)
        return char_stat

    def get_raw_characteristic_bonus(self, characteristic):
        characteristic_value = self.get_characteristic(characteristic)
        characteristic_bonus = get_tens(characteristic_value)
        return characteristic_bonus

    def get_modded_toughness_bonus(self, attack, hit_location=None):
        raw_bonus = self.get_raw_characteristic_bonus(STAT_TGH)
        extra_toughness = self.get_unnatural_characteristic(STAT_TGH)
        extra_toughness = Felling.handle_felling(attack, extra_toughness)
        extra_toughness = Daemonic.handle_daemonic(attack, extra_toughness)
        final_bonus = raw_bonus + extra_toughness
        if hit_location is not None:
            locational_toughness = self.get_locational_toughness(hit_location)
            final_bonus += locational_toughness
        return final_bonus

    def get_characteristic_bonus(self, characteristic):
        characteristic_bonus = self.get_raw_characteristic_bonus(
            characteristic)
        unnatural_bonus = self.get_unnatural_characteristic(
            characteristic)
        final_bonus = characteristic_bonus + unnatural_bonus
        return final_bonus

    def get_unnatural_characteristic(self, characteristic):
        trait_name = 'unnatural_{}'.format(characteristic)
        trait_value = self.modifiers.get(trait_name, 0)
        return trait_value

    @property
    def movement(self):
        move_mod = self.move_mod
        half_move = move_mod
        full_move = move_mod * 2
        charge_move = move_mod * 3
        run_move = move_mod * 6
        if self.sprint is not None:
            full_move += self.get_raw_characteristic_bonus(STAT_AGI)
            run_move = '{}/{}*'.format(run_move, run_move * 2)
        if self.preternatural_speed is not None:
            charge_move *= 2
        movement = {HALF_MOVE: half_move,
                    FULL_MOVE: full_move,
                    CHARGE_MOVE: charge_move,
                    RUN_MOVE: run_move}
        return movement

    @property
    def move_mod(self):
        agi_mod = self.get_characteristic_bonus(STAT_AGI)
        size_modifier = (self.size_trait - 4)
        move_mod = agi_mod + size_modifier
        if self.quadruped is not None:
            move_mod += agi_mod
        if self.jump_pack is not None:
            move_mod += agi_mod
        return move_mod

    @property
    def size_trait(self):
        return self.size if self.size is not None else 4

    @property
    def size_bonus(self):
        size_bonus = (self.size_trait * 10) - 40
        if self.black_carapace is not None and size_bonus > 0:
            size_bonus = 0
        return size_bonus

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
    def toughness(self):
        toughness = self.get_stat(STAT_TGH, default={})
        return toughness

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
