import json

import yaml


def pretty_print(dict_):
    print json.dumps(dict_, indent=4)


def read_definition(file_path):
    with open('C:\\Users\\Dos\'\\Desktop\\weapons.yml', 'r') as infile:
        something = yaml.load(infile)
        pretty_print(something)
