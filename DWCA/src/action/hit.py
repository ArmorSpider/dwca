

class Hit(object):

    def __init__(self, hit_location, damage, penetration):
        self.hit_location = hit_location
        self.damage = damage
        self.penetration = penetration

    def __str__(self, *args, **kwargs):
        return str('Hit({}, DMG: {}, PEN: {})').format(self.hit_location,
                                                       self.damage,
                                                       self.penetration)
