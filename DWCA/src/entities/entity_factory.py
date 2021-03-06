from src.dwca_log.log import get_log
from src.entities import VEHICLE
from src.entities.character import Character
from src.entities.horde import Horde
from src.entities.libraries import read_character, read_weapon
from src.entities.vehicle import Vehicle
from src.entities.weapon import Weapon


LOG = get_log(__name__)


def build_entity(entity_name, magnitude=None):
    definition = read_character(entity_name, best_match=True)
    if magnitude is not None:
        LOG.debug('"%s" is a horde.')
        return Horde(definition, magnitude)
    if definition.get(VEHICLE) is not None:
        LOG.debug('"%s" is a vehicle.')
        return Vehicle(definition)
    LOG.debug('"%s" is a character.')
    return Character(definition)


def build_weapon(weapon_name):
    definition = read_weapon(weapon_name, best_match=True)
    return Weapon(definition)
