from lazy.lazy import lazy

from definitions import WEAPON, ATTACKER, TARGET, DEFENSIVE_MODIFIERS,\
    RAW_WEAPON_STATS, HIT_LOCATIONS, MAGNITUDE_DAMAGE, EFFECTIVE_TOUGHNESS,\
    EFFECTIVE_ARMOR, BLOCKED, EFFECTIVE_DAMAGE, EFFECTIVE_PSY_RATING, NUM_HITS,\
    ROLLED_DAMAGE, RAW_DAMAGE, OFFENSIVE_MODIFIERS
from src.action.action import Action
from src.action.hit import Hit
from src.dwca_log.log import get_log
from src.entities import WOUNDS, ARMOR, DAMAGE_TYPE, DICE, PENETRATION,\
    FLAT_DAMAGE, TEARING_DICE, SWIFT_ATTACK, LIGHTNING_ATTACK
from src.entities.entity import Entity
from src.hit_location import FRONT, SIDE, REAR, get_hit_location_name
from src.hitloc_series import get_hit_locations
from src.modifiers.modifier import get_modifier, get_modifiers_iterator
from src.modifiers.qualities import Devastating, Hellfire
from src.roll_damage import roll_normal_damage, roll_righteous_fury,\
    handle_dos_minimum_damage
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def select_vehicle_hitloc():
    hit_locations = [FRONT, SIDE, REAR]
    LOG.info('Select vehicle hit location: ')
    hit_location = try_user_choose_from_list(hit_locations)
    return hit_location


def get_horde_bonus_dice(attack):
    attacker = attack.attacker
    horde_bonus_dice = 0
    if attacker.is_horde():
        if attacker.magnitude >= 10:
            LOG.debug('+1d10 from Horde with Magnitude >= 10.')
            horde_bonus_dice += 1
        if attacker.magnitude >= 20:
            LOG.debug('+1d10 from Horde with Magnitude >= 20.')
            horde_bonus_dice += 1
    return horde_bonus_dice


class Attack(Action):

    def __init__(self, weapon, attacker, target):
        Action.__init__(self)
        self.weapon = weapon if weapon is not None else Entity()
        self.attacker = attacker if attacker is not None else Entity()
        self.target = target if target is not None else Entity()
        self.ad_hoc_modifiers = {}

    def __getattr__(self, name):
        attribute = self.offensive_modifiers.get(name)
        if attribute is None and get_modifier(name) is None:
            return super(Attack, self).__getattribute__(name)
        else:
            return attribute

    def initialize_metadata(self):
        self.metadata[WEAPON] = self.weapon.name
        self.metadata[ATTACKER] = self.attacker.name
        self.metadata[TARGET] = self.target.name
        self.metadata[WOUNDS] = self.target.wounds
        self.metadata[ARMOR] = self.target.armor
        self.metadata[DAMAGE_TYPE] = self.weapon.damage_type
        self.metadata[DEFENSIVE_MODIFIERS] = self.target.modifiers
        self.metadata[RAW_WEAPON_STATS] = {DICE: self.weapon.dice,
                                           PENETRATION: self.weapon.penetration,
                                           FLAT_DAMAGE: self.weapon.flat_damage}

    @property
    def hit_location(self):
        if self.target.is_vehicle() is True:
            return select_vehicle_hitloc()
        else:
            return super(Attack, self).hit_location

    @property
    def hits(self):
        num_hits = self.num_hits
        LOG.debug('Attack scored %s hits.', num_hits)
        hit_locations = get_hit_locations(self.hit_location, num_hits)
        hits = []
        for hit_location in hit_locations:
            self.append_to_metadata(
                HIT_LOCATIONS, get_hit_location_name(hit_location))
            hit = Hit(hit_location=hit_location,
                      damage=self.raw_damage,
                      penetration=self.penetration)
            hits.append(hit)
        return hits

    def apply_attack(self):
        self.initialize_metadata()
        attack_total_damage = 0
        if self.is_successfull():
            attack_total_damage = self.apply_hits(self.hits)
        return attack_total_damage

    def apply_hits(self, hits):
        hit_damages = []
        for hit in hits:
            hit_damage = self.apply_hit(hit)
            hit_damages.append(hit_damage)
        attack_total_damage = sum(hit_damages)
        return attack_total_damage

    def apply_hit(self, hit):
        self.on_hit_effects()
        toughness = self.target.get_modded_toughness_bonus(
            self, hit.hit_location)
        effective_armor = self.get_effective_armor(hit)
        effective_damage = max(hit.damage - effective_armor - toughness, 0)
        effective_damage = self.on_damage_effects(effective_damage)
        is_blocked = self.is_hit_blocked()
        effective_damage = effective_damage if is_blocked is False else 0
        magnitude_damage = self.calculate_magnitude_damage(effective_damage)
        self.append_to_metadata(MAGNITUDE_DAMAGE, magnitude_damage)
        self.append_to_metadata(EFFECTIVE_TOUGHNESS, toughness)
        self.append_to_metadata(EFFECTIVE_ARMOR, effective_armor)
        self.append_to_metadata(BLOCKED, is_blocked)
        self.append_to_metadata(EFFECTIVE_DAMAGE, effective_damage)
        return effective_damage

    def calculate_magnitude_damage(self, effective_damage):
        if self.target.is_horde():
            magnitude_damage = min(1, effective_damage)
            if magnitude_damage > 0:
                magnitude_damage = Devastating.handle_devastating(
                    self, magnitude_damage)
                magnitude_damage = Hellfire.handle_hellfire_magnitude_damage(
                    self, magnitude_damage)
        else:
            magnitude_damage = 0
        return magnitude_damage

    def is_hit_blocked(self):
        force_field = self.target.force_field
        if self.non_damaging is not None:
            return False
        if force_field is not None and force_field.is_hit_blocked() is True:
            LOG.debug('Hit was blocked by force field.')
            return True
        else:
            return False

    @lazy
    def effective_psy_rating(self):
        psy_rating = self.psy_rating
        if psy_rating is not None:
            for modifier in self.modifer_iterator():
                psy_rating = modifier.modify_psy_rating(self, psy_rating)
            LOG.debug('Effective psy rating is %s.', psy_rating)
            self.update_metadata({EFFECTIVE_PSY_RATING: psy_rating})
            return psy_rating
        else:
            return None

    @lazy
    def tearing_dice(self):
        tearing_dice = 0
        for modifier in self.modifer_iterator():
            tearing_dice = modifier.modify_tearing_dice(self, tearing_dice)
        self.update_metadata({TEARING_DICE: tearing_dice})
        return tearing_dice

    @lazy
    def num_dice(self):
        num_dice = self.weapon.dice
        for modifier in self.modifer_iterator():
            num_dice = modifier.modify_num_dice(self, num_dice)
        num_dice += get_horde_bonus_dice(self)
        self.update_metadata({DICE: num_dice})
        return num_dice

    @lazy
    def penetration(self):
        penetration = self.weapon.penetration
        for modifier in self.modifer_iterator():
            penetration = modifier.modify_penetration(self, penetration)
        self.update_metadata({PENETRATION: penetration})
        return penetration

    @lazy
    def flat_damage(self):
        flat_damage = self.weapon.flat_damage
        for modifier in self.modifer_iterator():
            flat_damage = modifier.modify_damage(self, flat_damage)
        self.update_metadata({FLAT_DAMAGE: flat_damage})
        return flat_damage

    @lazy
    def num_hits(self):
        num_hits = 1
        for modifier in self.modifer_iterator():
            num_hits = modifier.modify_num_hits(self, num_hits)
        self.update_metadata({NUM_HITS: num_hits})
        return num_hits

    def modifer_iterator(self):
        modifiers = self.offensive_modifiers
        modifiers_iterator = get_modifiers_iterator(modifiers)
        return modifiers_iterator

    @property
    def rolled_damage(self):
        results = roll_normal_damage(self.num_dice, self.tearing_dice, self)
        results = roll_righteous_fury(results, self)
        results = handle_dos_minimum_damage(self, results)
        raw_rolled_damage = sum(results)
        LOG.debug('Rolled %s raw damage. (Rolls: %s)',
                  raw_rolled_damage, results)
        self.append_to_metadata(ROLLED_DAMAGE, results)
        return raw_rolled_damage

    @property
    def raw_damage(self):
        rolled_damage = self.rolled_damage
        flat_damage = self.flat_damage
        total_damage = rolled_damage + flat_damage
        LOG.debug('Total damage: %s. (Rolled: %s, Flat: %s)',
                  total_damage, rolled_damage, flat_damage)
        self.append_to_metadata(RAW_DAMAGE, total_damage)
        return total_damage

    @lazy
    def offensive_modifiers(self):
        LOG.debug('Getting offensive modifiers.')
        modifiers = {}
        modifiers.update(self.weapon.modifiers)
        modifiers.update(self.attacker.modifiers)
        modifiers.update(self.ad_hoc_modifiers)
        LOG.debug('Found %s offensive modifiers.', len(modifiers))
        self.update_metadata({OFFENSIVE_MODIFIERS: modifiers})
        return modifiers

    def get_effective_armor(self, hit):
        armor = self.target.get_armor(hit.hit_location)
        for modifier in self.modifer_iterator():
            armor = modifier.modify_armor(self, armor, hit.hit_location)
        effective_armor = max(armor - hit.penetration, 0)
        return effective_armor

    def on_hit_effects(self):
        for modifier in self.modifer_iterator():
            modifier.on_hit(self)

    def on_damage_effects(self, effective_damage):
        for modifier in self.modifer_iterator():
            effective_damage = modifier.on_damage(self, effective_damage)
        return effective_damage

    @property
    def firemodes(self):
        base_firemodes = self.weapon.firemodes
        if self.is_melee():
            if self.swift_attack is None:
                base_firemodes.pop(SWIFT_ATTACK, None)
            if self.lightning_attack is None:
                base_firemodes.pop(LIGHTNING_ATTACK, None)
        return base_firemodes

    def is_melee(self):
        return self.weapon.is_melee()

    def is_ranged(self):
        return self.weapon.is_ranged()

    def is_psychic(self):
        return self.weapon.is_psychic()
