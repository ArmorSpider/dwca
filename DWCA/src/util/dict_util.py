import json


def pretty_print(dict_):
    print json.dumps(dict_, indent=4)


def sort_strings_by_length(list_of_strings):
    sorted_list = reversed(sorted(list_of_strings, key=len))
    return sorted_list
