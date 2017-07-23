from collections import namedtuple
import re

from src.entities import NAME, DICE, DAMAGE, QUALITIES, PENETRATION, DAMAGE_TYPE,\
    WEAPON_CLASS
from src.util.read_file import pretty_print


WEAPON_CLASSES = ['Melee', 'Mounted', 'Basic', 'Heavy', 'Pistol', 'n/a']
RENOWN_RANKS = ['Famed', 'Distinguished', 'Respected']


def read_weapon_lines_file():
    with open('C:\\Users\\Dos\'\\Desktop\cooler_file.txt') as file_:
        file_lines = file_.readlines()
        weapon_lines = extract_weapon_lines(file_lines)
        pretty_print(weapon_lines)
        weapon_definitions = {}
        for weapon_line in weapon_lines:
            print weapon_line
            weapon_def, internal_name = build_weapon_definition(weapon_line)
            weapon_definitions[internal_name] = weapon_def
        pretty_print(weapon_definitions)
        return weapon_definitions


def extract_weapon_lines(file_lines):
    weapon_lines = []
    for line in file_lines:
        if 'd10' in line:
            clean_line = re.sub(r'([^\s\w\,()+/]|_)+', '', line).strip()
            clean_line = remove_renown_ranks(clean_line)
            clean_line = clean_line.replace('Full', '')
            weapon_lines.append(clean_line)
    return weapon_lines


def build_weapon_definition(weapon_line):
    print 'Building "{}"'.format(weapon_line)
    weapon_name, weapon_class = extract_name_and_class(weapon_line)
    damage_profile = extract_damage_profile(weapon_line)
    weapon_def = {
        NAME: weapon_name,
        WEAPON_CLASS: weapon_class,
        DICE: damage_profile.dice,
        DAMAGE: damage_profile.damage,
        DAMAGE_TYPE: damage_profile.damage_type,
        PENETRATION: damage_profile.penetration,
        QUALITIES: damage_profile.qualities
    }
    internal_name = extract_internal_name(weapon_name)
    return weapon_def, internal_name


def extract_internal_name(weapon_name):
    return weapon_name.lower().strip().replace(' ', '_')


def extract_damage_profile(weapon_line):
    DamageProfile = namedtuple(
        'DmgProfile', ['dice', 'damage', 'penetration', 'damage_type', 'qualities'])
    matches = re.findall(
        r'(\d)d10\+*(\d*)\s?([IREX])\s?(\d*)[\W\d]*(\w.*)?(\d|$)', weapon_line)[0]
    dice = int(matches[0])
    damage = int(matches[1] if matches[1] != '' else 0)
    damage_type = matches[2]
    penetration = int(matches[3] if matches[3] != '' else 0)
    qualities_list = matches[4].split(',')
    qualities_dict = convert_qualities_list_to_dict(qualities_list)
    damage_profile = DamageProfile(dice=dice,
                                   damage=damage,
                                   damage_type=damage_type,
                                   penetration=penetration,
                                   qualities=qualities_dict)
    return damage_profile


def remove_renown_ranks(weapon_line):
    for renown_string in RENOWN_RANKS:
        weapon_line = weapon_line.replace(renown_string, '')
    return weapon_line


def convert_qualities_list_to_dict(qualities_list):
    qualities_dict = {}
    for quality in qualities_list:
        if '(' not in quality:
            quality_value = True
        else:
            quality_value = int(re.findall(r'(\d)', quality)[0])
        quality_name = re.sub(
            r'([^\sa-zA-Z]|_)+', '', quality).strip().lower()
        if quality_name != '':
            qualities_dict[quality_name] = quality_value
    return qualities_dict


def extract_name_and_class(weapon_line):
    for weapon_class in WEAPON_CLASSES:
        split_list = weapon_line.split(weapon_class)
        if len(split_list) > 1:
            name = split_list[0].strip()
            return name, weapon_class
