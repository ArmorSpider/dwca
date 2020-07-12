from _functools import partial
from functools import lru_cache
import os

import yaml

from definitions import ROOT_DIR
from src.dwca_log.log import get_log


CONTENT_PATH = os.path.join(ROOT_DIR, "content")
LOG = get_log(__name__)


def read_file(file_path):
    with open(file_path, "r") as infile:
        file_content = yaml.safe_load(infile)
    if file_content is None:
        file_content = {}
    return file_content


def read_files(file_paths):
    combined_content = {}
    for file_path in file_paths:
        combined_content.update(read_file(file_path))
    return combined_content


def get_files_in_dir(dir_path, prefix=None):
    file_paths = []
    for file_ in os.listdir(dir_path):
        if file_.endswith(".yml") and (prefix is None or file_.startswith(prefix)):
            file_paths.append(os.path.join(dir_path, file_))
    return file_paths


@lru_cache
def read_dospedia():
    file_path = os.path.join(CONTENT_PATH, "dospedia.yml")
    dospedia = read_file(file_path)
    return dospedia


@lru_cache
def read_character_library():
    file_paths = get_character_files()
    character_library = read_files(file_paths)
    return character_library


@lru_cache
def read_weapon_library():
    file_paths = get_weapon_files()
    weapon_library = read_files(file_paths)
    return weapon_library


def write_dict_to_yaml_file(dict_, file_path):
    with open(file_path, "w") as outfile:
        yaml.dump(dict_, outfile)


get_character_files = partial(get_files_in_dir, CONTENT_PATH, "characters")
get_weapon_files = partial(get_files_in_dir, CONTENT_PATH, "weapons")
