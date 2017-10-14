from enum import Enum
from src.dwca_log.log import get_log
from src.util.string_util import normalize_string

LOG = get_log(__name__)


class Species(Enum):
    HUMAN = 'human'
    TYRANID = 'tyranid'
    ORK = 'ork'
    TAU = 'tau'
    DAEMON = 'daemon'
    ELDAR = 'eldar'
    NECRON = 'necron'
    XENO = 'xeno'


def is_alien_species(species_string):
    species = identify_species(species_string)
    is_alien = species in get_alien_species()
    LOG.debug('Is "%s" alien? %s.', species_string, is_alien)
    return is_alien


def identify_species(species_string):
    species_result = Species.XENO
    for species in list(Species):
        if normalize_string(species_string) == species.value:
            species_result = species
    LOG.debug('"%s" identified as %s.', species_string, species_result)
    return species_result


def get_alien_species():
    return [Species.TYRANID,
            Species.TAU,
            Species.ORK,
            Species.ELDAR,
            Species.XENO]
