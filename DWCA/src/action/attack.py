from src.action.action import Action
from src.action.hit import Hit
from src.dwca_log.log import get_log
from src.entities import TRAITS, TALENTS, QUALITIES, DICE, PENETRATION, DAMAGE
from src.hitloc_series import get_hit_locations
from src.modifiers.modifier import get_modifiers_iterator
from src.roll_damage import roll_normal_damage, roll_righteous_fury


LOG = get_log(__name__)


class Attack(Action):

    def __init__(self, weapon, attacker, target):
        Action.__init__(self)
        self.weapon = weapon
        self.attacker = attacker
        self.target = target
        self.num_dice = None
        self.tearing_dice = None
        self.penetration = None
        self.flat_damage = None
        self.num_hits = None

    def hits_generator(self):
        num_hits = self._get_num_hits()
        LOG.info('Attack scored %s hits.', num_hits)
        hit_locations = get_hit_locations(self.get_hit_location(), num_hits)
        for hit_location in hit_locations:
            hit = Hit(hit_location=hit_location,
                      damage=self._roll_damage(),
                      penetration=self._get_penetration())
            yield hit

    def apply_hits(self):
        attack_total_damage = 0
        if self.is_successfull():
            for hit in self.hits_generator():
                attack_total_damage += self.get_target().mitigate_hit(self, hit)
        return attack_total_damage

    def _get_num_hits(self):
        if self.num_hits is not None:
            num_hits = self.num_hits
        else:
            num_hits = self._calculate_num_hits()
            self.num_hits = num_hits
        LOG.debug('Num hits is %s.', num_hits)
        return num_hits

    def _get_num_dice(self):
        if self.num_dice is not None:
            num_dice = self.num_dice
        else:
            num_dice = self._calculate_num_dice()
            self.num_dice = num_dice
        LOG.debug('Num dice is %s.', num_dice)
        return num_dice

    def _get_tearing_dice(self):
        if self.tearing_dice is not None:
            tearing_dice = self.tearing_dice
        else:
            tearing_dice = self._calculate_tearing_dice()
            self.tearing_dice = tearing_dice
        LOG.debug('Tearing dice is %s.', tearing_dice)
        return tearing_dice

    def _get_penetration(self):
        if self.penetration is not None:
            penetration = self.penetration
        else:
            penetration = self._calculate_penetration()
            self.penetration = penetration
        LOG.debug('Penetration is %s.', penetration)
        return penetration

    def _get_flat_damage(self):
        if self.flat_damage is not None:
            flat_damage = self.flat_damage
        else:
            flat_damage = self._calculate_flat_damage()
            self.flat_damage = flat_damage
        LOG.debug('Flat damage is %s.', flat_damage)
        return flat_damage

    def get_weapon(self):
        return self.weapon

    def get_attacker(self):
        return self.attacker

    def get_target(self):
        return self.target

    def _offensive_modifiers(self):
        modifiers = self._combine_offensive_modifiers()
        modifiers_iterator = get_modifiers_iterator(modifiers)
        return modifiers_iterator

    def _calculate_num_dice(self):
        num_dice = self.get_weapon_stat(DICE, default=1)
        for modifier in self._offensive_modifiers():
            num_dice = modifier.modify_num_dice(self, num_dice)
        return num_dice

    def _calculate_tearing_dice(self):
        tearing_dice = 0
        for modifier in self._offensive_modifiers():
            tearing_dice = modifier.modify_tearing_dice(self, tearing_dice)
        return tearing_dice

    def _calculate_penetration(self):
        penetration = self.get_weapon_stat(PENETRATION, default=0)
        for modifier in self._offensive_modifiers():
            penetration = modifier.modify_penetration(self, penetration)
        return penetration

    def _calculate_flat_damage(self):
        flat_damage = self.get_weapon_stat(DAMAGE, default=0)
        for modifier in self._offensive_modifiers():
            flat_damage = modifier.modify_damage(self, flat_damage)
        return flat_damage

    def _calculate_num_hits(self):
        num_hits = 1
        for modifier in self._offensive_modifiers():
            num_hits = modifier.modify_num_hits(self, num_hits)
        return num_hits

    def _roll_raw_damage(self):
        real_dice = self._get_num_dice()
        tearing_dice = self._get_tearing_dice()
        results = roll_normal_damage(real_dice, tearing_dice)
        results = roll_righteous_fury(results, self)
        raw_rolled_damage = sum(results)
        LOG.debug('Rolled %s raw damage. (Rolls: %s)',
                  raw_rolled_damage, results)
        return raw_rolled_damage

    def _roll_damage(self):
        LOG.info('Rolling damage!')
        rolled_damage = self._roll_raw_damage()
        flat_damage = self._get_flat_damage()
        total_damage = rolled_damage + flat_damage
        LOG.info('Total damage: %s. (Rolled: %s, Flat: %s)',
                 total_damage, rolled_damage, flat_damage)
        return total_damage

    def _combine_offensive_modifiers(self):
        LOG.debug('Getting offensive modifiers.')
        modifiers = {}
        modifiers.update(self.get_weapon_stat(QUALITIES, default={}))
        modifiers.update(self.get_attacker_stat(TRAITS, default={}))
        modifiers.update(self.get_attacker_stat(TALENTS, default={}))
        LOG.debug('Found %s offensive modifiers.', len(modifiers))
        return modifiers

    def is_melee(self):
        return self.get_weapon().is_melee()

    def is_ranged(self):
        return self.get_weapon().is_melee() is not True

    def get_num_attacks(self):
        attacker = self.get_attacker()
        if self.is_melee():
            return attacker.get_num_melee_attacks()
        else:
            return attacker.get_num_ranged_attacks()

    def get_target_stat(self, stat_name, default=None):
        return self.get_target().get_stat(stat_name, default)

    def get_attacker_stat(self, stat_name, default=None):
        return self.get_attacker().get_stat(stat_name, default)

    def get_weapon_stat(self, stat_name, default=None):
        return self.get_weapon().get_stat(stat_name, default)
