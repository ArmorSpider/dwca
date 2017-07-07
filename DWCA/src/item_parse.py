import re

from src.util.read_file import pretty_print


CLASSES = ['Melee', 'Mounted']


def hi():
    with open('C:\\Users\\Dos\'\\Desktop\cool_file.txt') as file_:
        content = file_.readlines()
        content = [x.strip() for x in content]
        content = [x.replace('\u2020', '') for x in content]
        weapon_lines = []
        for line in content:
            if 'd10' in line:
                clean_line = re.sub(r'([^\s\w\,()+]|_)+', '', line)
                weapon_lines.append(clean_line)
        pretty_print(weapon_lines)

        for weapon_line in weapon_lines:
            name, weapon_class = find_name(weapon_line)
            stuff = re.findall(
                r'(\d)d10\+*(\d*) ([IREX]) (\d*) (\w.*)?\s\d+\s\d+', weapon_line)[0]
            dice = stuff[0]
            flat_damage = stuff[1]
            damage_type = stuff[2]
            penetration = stuff[3]
            qualities = stuff[4]
            print name
            print weapon_class
            print '{}d10+{} {} Pen: {} Qual: {}'.format(dice, flat_damage, damage_type, penetration, qualities)


def find_name(weapon_line):
    for weapon_class in CLASSES:
        split_list = weapon_line.split(weapon_class)
        if len(split_list) > 1:
            return split_list[0], weapon_class
