from src.action.action import Action
from src.modifiers.modifier import get_modifier
from src.dwca_log.log import get_log
from src.entities import TRAITS, TALENTS, QUALITIES, DICE, PENETRATION, DAMAGE


LOG = get_log(__name__)


class Attack(Action):

    def __init__(self, weapon, attacker, target):
        self.weapon = weapon
        self.attacker = attacker
        self.target = target

    def get_weapon(self):
        return self.weapon

    def get_attacker(self):
        return self.attacker

    def get_target(self):
        return self.target

    def offensive_modifiers(self):
        modifiers = self._combine_offensive_modifiers()
        modifiers_iterator = self._get_modifiers_iterator(modifiers)
        return modifiers_iterator

    def defensive_modifiers(self):
        modifiers = self._combine_defensive_modifiers()
        modifiers_iterator = self._get_modifiers_iterator(modifiers)
        return modifiers_iterator

    def _get_modifiers_iterator(self, modifiers_dict):
        for modifier_name in modifiers_dict:
            modifier = get_modifier(modifier_name)
            if modifier is not None:
                yield modifier

    def calculate_num_dice(self):
        num_dice = self.get_weapon_stat(DICE)
        # TODO: Calculate modifiers!
        return num_dice

    def calculate_penetration(self):
        penetration = self.get_weapon_stat(PENETRATION)
        for modifier in self.offensive_modifiers():
            penetration = modifier.modify_penetration(self, penetration)
        return penetration

    def calculate_flat_damage(self):
        flat_damage = self.get_weapon_stat(DAMAGE)
        for modifier in self.offensive_modifiers():
            flat_damage = modifier.modify_damage(self, flat_damage)
        LOG.debug('Flat damage is {}'.format(flat_damage))
        return flat_damage

    def _combine_defensive_modifiers(self):
        LOG.debug('Getting  modifiers.')
        modifiers = {}
        modifiers.update(self.get_target_stat(TRAITS))
        modifiers.update(self.get_target_stat(TALENTS))
        LOG.debug('Found {} defensive modifiers.'.format(len(modifiers)))
        return modifiers

    def _combine_offensive_modifiers(self):
        LOG.debug('Getting offensive modifiers.')
        modifiers = {}
        modifiers.update(self.get_weapon_stat(QUALITIES))
        modifiers.update(self.get_attacker_stat(TRAITS))
        modifiers.update(self.get_attacker_stat(TALENTS))
        LOG.debug('Found {} offensive modifiers.'.format(len(modifiers)))
        return modifiers

    def is_melee(self):
        return False

    def get_target_stat(self, stat_name):
        return self._get_entity_stat(self.get_target(), stat_name)

    def get_attacker_stat(self, stat_name):
        return self._get_entity_stat(self.get_attacker(), stat_name)

    def get_weapon_stat(self, stat_name):
        return self._get_entity_stat(self.get_weapon(), stat_name)

    def _get_entity_stat(self, entity, stat_name):
        stat = entity.get_stat(stat_name)
        return stat
