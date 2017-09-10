import difflib
import os

import yaml

from definitions import ROOT_DIR
from src.dwca_log.log import get_log
from src.errors import WeaponNotFoundError
from src.util.string_util import convert_to_snake_case


CONTENT_PATH = os.path.join(ROOT_DIR, 'content')
LOG = get_log(__name__)


def read_file(file_path):
    with open(file_path, 'r') as infile:
        file_content = yaml.load(infile)
        return file_content


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
    cleaned_name = convert_to_snake_case(character_name)
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
        best_match = None
    return best_match


def find_best_weapon_match(weapon_name):
    cleaned_name = convert_to_snake_case(weapon_name)
    available_weapons = get_weapon_library().keys()
    best_match = find_best_match(cleaned_name, available_weapons)
    LOG.debug('Best match for "%s" is "%s"', weapon_name, best_match)
    return best_match


def get_character_library():
    file_path = os.path.join(CONTENT_PATH, 'characters.yml')
    character_library = read_file(file_path)
    return character_library


def get_weapon_library():
    file_path = os.path.join(CONTENT_PATH, 'weapons.yml')
    weapon_library = read_file(file_path)
    return weapon_library


def read_character(character_name, best_match=True):
    if best_match is True:
        character_name = find_best_character_match(character_name)
    character_library = get_character_library()
    try:
        character_definition = character_library[character_name]
        return character_definition
    except KeyError:
        print '"{}" not available.'.format(character_name)


def write_dict_to_yaml_file(dict_, file_path):
    with open(file_path, 'w') as outfile:
        yaml.dump(dict_, outfile)
