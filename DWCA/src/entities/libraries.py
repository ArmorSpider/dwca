import difflib

from src.dwca_log.log import get_log
from src.errors import WeaponNotFoundError, NoMatchError
from src.util.read_file import read_weapon_library, read_character_library
from src.util.string_util import normalize_string


LOG = get_log(__name__)


class MasterLibrary(object):

    weapon_library = read_weapon_library()
    character_library = read_character_library()


def get_weapon_library():
    return MasterLibrary.weapon_library


def get_character_library():
    return MasterLibrary.character_library


def read_character(character_name, best_match=True):
    if best_match is True:
        character_name = find_best_character_match(character_name)
    character_library = get_character_library()
    try:
        character_definition = character_library[character_name]
        return character_definition
    except KeyError:
        print '"{}" not available.'.format(character_name)


def read_weapon(weapon_name, best_match=True):
    if best_match is True:
        weapon_name = find_best_weapon_match(weapon_name)
    weapon_library = get_weapon_library()
    try:
        weapon_definition = weapon_library[weapon_name]
        return weapon_definition
    except KeyError:
        print '"{}" not available.'.format(weapon_name)
        raise WeaponNotFoundError


def find_best_character_match(character_name):
    cleaned_name = normalize_string(character_name)
    available_characters = get_character_library().keys()
    best_match = find_best_match(cleaned_name, available_characters)
    LOG.debug('Best match for "%s" is "%s"', character_name, best_match)
    return best_match


def find_best_match(input_string, options):
    results = difflib.get_close_matches(
        input_string, options, n=1)
    if len(results) >= 1:
        best_match = results[0]
    else:
        raise NoMatchError('No match found for %s.' % input_string)
    return best_match


def find_best_weapon_match(weapon_name):
    cleaned_name = normalize_string(weapon_name)
    available_weapons = get_weapon_library().keys()
    best_match = find_best_match(cleaned_name, available_weapons)
    LOG.debug('Best match for "%s" is "%s"', weapon_name, best_match)
    return best_match
