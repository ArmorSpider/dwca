from src.dwca_log.log import get_log

LOG = get_log(__name__)


class Hit(object):

    def __init__(self, hit_location, damage, penetration):
        self.hit_location = hit_location
        self.damage = int(damage)
        self.penetration = int(penetration)

    def calculate_effective_damage(self, armor, toughness):
        effective_armor = max(armor - self.penetration, 0)
        LOG.info('Effective armor is %s. (%s Armor - %s Penetration)',
                 effective_armor, armor, self.penetration)
        effective_damage = max(self.damage - effective_armor - toughness, 0)
        LOG.info('Effective damage is %s. (%s damage - %s Armor - %s Toughness)',
                 effective_damage, self.damage, effective_armor, toughness)
        return effective_damage

    def __str__(self, *args, **kwargs):
        return str('Hit({}, DMG: {}, PEN: {})').format(self.hit_location,
                                                       self.damage,
                                                       self.penetration)
