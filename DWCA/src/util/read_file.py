import os

import yaml
from definitions import ROOT_DIR


CONTENT_PATH = os.path.join(ROOT_DIR, 'content')


def read_file(file_path):
    with open(file_path, 'r') as infile:
        something = yaml.load(infile)
        return something


def read_weapon(weapon_name):
    file_path = os.path.join(CONTENT_PATH, 'weapons.yml')
    weapon_library = read_file(file_path)
    try:
        weapon_definition = weapon_library[weapon_name]
        return weapon_definition
    except KeyError:
        print '"{}" not available.'.format(weapon_name)


def read_character(character_name):
    file_path = os.path.join(CONTENT_PATH, 'characters.yml')
    character_library = read_file(file_path)
    try:
        character_definition = character_library[character_name]
        return character_definition
    except KeyError:
        print '"{}" not available.'.format(character_name)


def write_dict_to_yaml_file(dict_, file_path):
    with open(file_path, 'w') as outfile:
        yaml.dump(dict_, outfile)
