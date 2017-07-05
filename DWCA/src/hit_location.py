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
