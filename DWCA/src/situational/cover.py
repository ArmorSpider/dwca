from src.dwca_log.log import get_log
from src.hit_location import BODY, RIGHT_LEG, LEFT_LEG
from src.situational.state_manager import StateManager


LOG = get_log(__name__)


def is_hitloc_eligible_for_cover(hit_location):
    result = hit_location in [BODY, RIGHT_LEG, LEFT_LEG]
    LOG.debug('Is %s eligible for cover? %s', hit_location, result)
    return result


def get_cover_armor_for_hitloc(hit_location):
    cover_armor = StateManager.cover
    if is_hitloc_eligible_for_cover(hit_location) and cover_armor > 0:
        LOG.info('Cover armor for %s is %s.', hit_location, cover_armor)
        return cover_armor
    else:
        return 0
