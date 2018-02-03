from src.dwca_log.log import get_log

LOG = get_log(__name__)


class Hit(object):

    def __init__(self, hit_location, damage, penetration):
        self.hit_location = hit_location
        self.damage = int(damage)
        self.penetration = int(penetration)

    def __str__(self, *args, **kwargs):
        return str('Hit({}, DMG: {}, PEN: {})').format(self.hit_location,
                                                       self.damage,
                                                       self.penetration)
