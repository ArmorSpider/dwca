from collections import namedtuple
import re

from src.entities import NAME, DICE, DAMAGE, QUALITIES
from src.util.read_file import pretty_print


WEAPON_CLASSES = ['Melee', 'Mounted']
RENOWN_RANKS = ['Famed', 'Distinguished', 'Respected']


def hi():
    with open('C:\\Users\\Dos\'\\Desktop\cool_file.txt') as file_:
        content = file_.readlines()
        content = [x.strip() for x in content]
        content = [x.replace('\u2020', '') for x in content]
        weapon_lines = []
        for line in content:
            if 'd10' in line:
                clean_line = re.sub(r'([^\s\w\,()+]|_)+', '', line)
                clean_line = remove_renown_ranks(clean_line)
                weapon_lines.append(clean_line)
        weapon_definitions = {}
        for weapon_line in weapon_lines:
            name, weapon_class = extract_name_and_class(weapon_line)
            damage_profile = extract_damage_profile(weapon_line)
            qualities = convert_qualities_list_to_dict(
                damage_profile.qualities)
            weapon_def = {
                NAME: name,
                'class': weapon_class,
                DICE: damage_profile.dice,
                DAMAGE: damage_profile.damage,
                'damage_type': damage_profile.damage_type,
                'penetration': damage_profile.penetration,
                QUALITIES: qualities
            }
            internal_name = name.lower().strip().replace(' ', '_')

            weapon_definitions[internal_name] = weapon_def
        pretty_print(weapon_definitions)
        return weapon_definitions


def extract_damage_profile(weapon_line):
    DamageProfile = namedtuple(
        'DmgProfile', ['dice', 'damage', 'penetration', 'damage_type', 'qualities'])
    matches = re.findall(
        r'(\d)d10\+*(\d*) ([IREX]) (\d*) ?(\w.*)?(\d|$)', weapon_line)[0]
    damage_profile = DamageProfile(dice=int(matches[0]),
                                   damage=int(
                                       matches[1] if matches[1] != '' else 0),
                                   damage_type=matches[2],
                                   penetration=int(matches[
                                       3] if matches[3] != '' else 0),
                                   qualities=matches[4].split(','))
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
