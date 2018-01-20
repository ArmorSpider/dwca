from random import choice

from src.dwca_log.log import get_log
from src.util.rand_util import roll_die


LOG = get_log(__name__)


def scatter():
    directions = ['NW', 'N', 'NE', 'E', 'SE', 'SE', 'S', 'SW', 'SW']
    scatter_direction = choice(directions)
    scatter_distance = roll_die(10)
    LOG.info('SCATTER: %sm %s.', scatter_distance, scatter_direction)
