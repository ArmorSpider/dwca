import difflib

from definitions import CLASS, MELEE
from src.dwca_log.log import get_log
from src.entities import PACKAGE, NAME, DICE, DAMAGE_TYPE, PENETRATION, RANGE,\
    FLAT_DAMAGE
from src.errors import WeaponNotFoundError, NoMatchError
from src.util.read_file import read_weapon_library, read_character_library
from src.util.string_util import normalize_string


LOG = get_log(__name__)

DEFAULT_PACKAGE = 'default'


def verify_weapons():
    require_all = [CLASS, NAME, DICE, FLAT_DAMAGE, DAMAGE_TYPE, PENETRATION]
    ranged_only = require_all + [RANGE]
    MasterLibrary.load_all_packages()
    for weapon_name, weapon_def in get_weapon_library().iteritems():
        missing_keys = []
        is_melee = weapon_def.get(CLASS, 'NO_CLASS').lower() == MELEE
        if is_melee:
            required = require_all
        else:
            required = ranged_only
        for key in required:
            if key not in weapon_def:
                missing_keys.append(key)
        if missing_keys != []:
            print '______[%s]______' % weapon_name
            print weapon_def.get('_package', DEFAULT_PACKAGE)
            for key in missing_keys:
                print '%s is missing %s' % (weapon_name, key)


class MasterLibrary(object):

    weapon_library = read_weapon_library()
    character_library = read_character_library()
    available_packages = [DEFAULT_PACKAGE]

    @staticmethod
    def add_character(char_key, char_def):
        LOG.debug('Manually added "%s" to character library.', char_key)
        MasterLibrary.character_library[char_key] = char_def

    @staticmethod
    def add_weapon(weapon_key, weapon_def):
        LOG.debug('Manually added "%s" to weapon library.', weapon_key)
        MasterLibrary.weapon_library[weapon_key] = weapon_def

    @staticmethod
    def load_all_packages():
        for package in MasterLibrary.get_known_packages():
            MasterLibrary.add_package(package)

    @staticmethod
    def get_known_packages():
        known_packages = []
        for entity_def in MasterLibrary.weapon_library.values():
            package = entity_def.get(PACKAGE, DEFAULT_PACKAGE)
            known_packages.append(package)
        for entity_def in MasterLibrary.character_library.values():
            package = entity_def.get(PACKAGE, DEFAULT_PACKAGE)
            known_packages.append(package)
        known_packages = list(set(known_packages))
        return known_packages

    @staticmethod
    def get_loaded_packages():
        return MasterLibrary.available_packages

    @staticmethod
    def filter_library(library_dict):
        filtered_library = {}
        for entity_name, entity_def in library_dict.iteritems():
            weapon_package = entity_def.get(PACKAGE, DEFAULT_PACKAGE)
            if weapon_package in MasterLibrary.available_packages:
                filtered_library[entity_name] = entity_def
        return filtered_library

    @staticmethod
    def add_package(package_name):
        LOG.info('Added "%s" package.', package_name)
        MasterLibrary.available_packages.append(package_name)

    @staticmethod
    def reload_libraries(self):
        LOG.info('Reloaded libraries.')
        MasterLibrary.weapon_library = read_weapon_library()
        MasterLibrary.character_library = read_character_library()


def get_weapon_library():
    filtered_library = MasterLibrary.filter_library(
        MasterLibrary.weapon_library)
    return filtered_library


def get_character_library():
    filtered_library = MasterLibrary.filter_library(
        MasterLibrary.character_library)
    return filtered_library


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
