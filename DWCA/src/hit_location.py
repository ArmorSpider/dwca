
from enum import Enum


class HitLocation(Enum):
    HEAD = 10
    RIGHT_ARM = 20
    LEFT_ARM = 30
    BODY = 70
    RIGHT_LEG = 85
    LEFT_LEG = 100


def get_hit_location(reversed_roll):
    for hit_location in list(HitLocation):
        if reversed_roll <= hit_location.value:
            return hit_location
    raise ValueError('{} is not a supported HitLocation'.format(reversed_roll))


def get_hit_location_name(hit_location):
    return hit_location.name.lower()


HEAD = HitLocation.HEAD
BODY = HitLocation.BODY
LEFT_ARM = HitLocation.LEFT_ARM
RIGHT_ARM = HitLocation.RIGHT_ARM
LEFT_LEG = HitLocation.LEFT_LEG
RIGHT_LEG = HitLocation.RIGHT_LEG
HITLOC_HEAD = get_hit_location_name(HitLocation.HEAD)
HITLOC_RIGHT_ARM = get_hit_location_name(HitLocation.RIGHT_ARM)
HITLOC_LEFT_ARM = get_hit_location_name(HitLocation.LEFT_ARM)
HITLOC_BODY = get_hit_location_name(HitLocation.BODY)
HITLOC_RIGHT_LEG = get_hit_location_name(HitLocation.RIGHT_LEG)
HITLOC_LEFT_LEG = get_hit_location_name(HitLocation.LEFT_LEG)
HITLOC_ALL = 'all'
