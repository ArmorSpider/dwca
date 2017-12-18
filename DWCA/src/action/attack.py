from lazy.lazy import lazy

from definitions import ATTACKER, TARGET, WEAPON, NUM_HITS, ROLLED_DAMAGE,\
    TOTAL_DAMAGE, OFFENSIVE_MODIFIERS
from src.action.action import Action
from src.action.hit import Hit
from src.dwca_log.log import get_log
from src.entities import DICE, PENETRATION, FLAT_DAMAGE,\
    TEARING_DICE
from src.entities.entity import Entity
from src.hitloc_series import get_hit_locations
from src.modifiers.modifier import get_modifiers_iterator, get_modifier
from src.roll_damage import roll_normal_damage, roll_righteous_fury


LOG = get_log(__name__)


class Attack(Action):

    def __init__(self, weapon, attacker, target):
        Action.__init__(self)
        self.weapon = weapon if weapon is not None else Entity()
        self.attacker = attacker if attacker is not None else Entity()
        self.target = target if target is not None else Entity()
        self.ad_hoc_modifiers = {}
        self.metadata[WEAPON] = self.weapon.name
        self.metadata[ATTACKER] = self.attacker.name
        self.metadata[TARGET] = self.target.name

    def __getattr__(self, name):
        attribute = self.offensive_modifiers.get(name)
        if attribute is None and get_modifier(name) is None:
            return super(Attack, self).__getattribute__(name)
        else:
            return attribute

    def hits_generator(self):
        num_hits = self.num_hits
        LOG.info('Attack scored %s hits.', num_hits)
        hit_locations = get_hit_locations(self.get_hit_location(), num_hits)
        for hit_location in hit_locations:
            hit = Hit(hit_location=hit_location,
                      damage=self.total_damage,
                      penetration=self.penetration)
            yield hit

    def apply_hits(self, custom_hits=None):
        attack_total_damage = 0
        hit_damages = []
        if self.is_successfull():
            force_field = self.target.force_field
            if custom_hits is None:
                hits = self.hits_generator()
            else:
                hits = custom_hits
            for index, hit in enumerate(hits):
                LOG.info('[Hit %s]', index + 1)
                if force_field is not None:
                    if force_field.is_hit_blocked() is True:
                        LOG.info('Blocked by force field.')
                        continue
                hit_damage = self.target.mitigate_hit(self, hit)
                hit_damages.append(hit_damage)
            attack_total_damage = sum(hit_damages)
            LOG.info('All hits combined damage: %s (%s)', attack_total_damage,
                     ' + '.join([str(hit_damage) for hit_damage in hit_damages]))
        return attack_total_damage

    @lazy
    def tearing_dice(self):
        tearing_dice = 0
        for modifier in self.modifer_iterator():
            tearing_dice = modifier.modify_tearing_dice(self, tearing_dice)
        self._update_metadata({TEARING_DICE: tearing_dice})
        return tearing_dice

    @lazy
    def num_dice(self):
        num_dice = self.weapon.dice
        for modifier in self.modifer_iterator():
            num_dice = modifier.modify_num_dice(self, num_dice)
        self._update_metadata({DICE: num_dice})
        return num_dice

    @lazy
    def penetration(self):
        penetration = self.weapon.penetration
        for modifier in self.modifer_iterator():
            penetration = modifier.modify_penetration(self, penetration)
        self._update_metadata({PENETRATION: penetration})
        return penetration

    @lazy
    def flat_damage(self):
        flat_damage = self.weapon.flat_damage
        for modifier in self.modifer_iterator():
            flat_damage = modifier.modify_damage(self, flat_damage)
        self._update_metadata({FLAT_DAMAGE: flat_damage})
        return flat_damage

    @lazy
    def num_hits(self):
        num_hits = 1
        for modifier in self.modifer_iterator():
            num_hits = modifier.modify_num_hits(self, num_hits)
        self._update_metadata({NUM_HITS: num_hits})
        return num_hits

    def modifer_iterator(self):
        modifiers = self.offensive_modifiers
        modifiers_iterator = get_modifiers_iterator(modifiers)
        return modifiers_iterator

    @property
    def rolled_damage(self):
        results = roll_normal_damage(self.num_dice, self.tearing_dice, self)
        results = roll_righteous_fury(results, self)
        raw_rolled_damage = sum(results)
        LOG.info('Rolled %s raw damage. (Rolls: %s)',
                 raw_rolled_damage, results)
        self._append_to_metadata(ROLLED_DAMAGE, raw_rolled_damage)
        return raw_rolled_damage

    @property
    def total_damage(self):
        rolled_damage = self.rolled_damage
        flat_damage = self.flat_damage
        total_damage = rolled_damage + flat_damage
        LOG.debug('Total damage: %s. (Rolled: %s, Flat: %s)',
                  total_damage, rolled_damage, flat_damage)
        self._append_to_metadata(TOTAL_DAMAGE, total_damage)
        return total_damage

    @lazy
    def offensive_modifiers(self):
        LOG.debug('Getting offensive modifiers.')
        modifiers = {}
        modifiers.update(self.weapon.modifiers)
        modifiers.update(self.attacker.modifiers)
        modifiers.update(self.ad_hoc_modifiers)
        LOG.debug('Found %s offensive modifiers.', len(modifiers))
        self._update_metadata({OFFENSIVE_MODIFIERS: modifiers})
        return modifiers

    def get_effective_armor(self, hit_location):
        armor = self.target.get_armor(hit_location)
        for modifier in self.modifer_iterator():
            armor = modifier.modify_armor(self, armor)
        return armor

    def on_hit_effects(self):
        for modifier in self.modifer_iterator():
            modifier.on_hit(self)

    def on_damage_effects(self, effective_damage):
        for modifier in self.modifer_iterator():
            modifier.on_damage(self, effective_damage)

    def is_melee(self):
        return self.weapon.is_melee()

    def is_ranged(self):
        return self.weapon.is_melee() is not True
