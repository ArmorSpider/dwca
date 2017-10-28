import os

import yaml

from definitions import ROOT_DIR
from src.dwca_log.log import get_log


CONTENT_PATH = os.path.join(ROOT_DIR, 'content')
LOG = get_log(__name__)


def read_file(file_path):
    with open(file_path, 'r') as infile:
        file_content = yaml.load(infile)
        return file_content


def read_dospedia():
    file_path = os.path.join(CONTENT_PATH, 'dospedia.yml')
    dospedia = read_file(file_path)
    return dospedia


def read_character_library():
    file_path = os.path.join(CONTENT_PATH, 'characters.yml')
    character_library = read_file(file_path)
    return character_library


def read_weapon_library():
    file_path = os.path.join(CONTENT_PATH, 'weapons.yml')
    weapon_library = read_file(file_path)
    return weapon_library


def write_dict_to_yaml_file(dict_, file_path):
    with open(file_path, 'w') as outfile:
        yaml.dump(dict_, outfile)
