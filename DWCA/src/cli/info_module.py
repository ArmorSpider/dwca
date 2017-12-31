from src.cli.table import print_table, print_entity_dict
from src.entities import SKILLS, CHARACTERISTICS
from src.entities.character import get_char
from src.entities.libraries import get_character_library
from src.util.dict_util import sort_strings_by_length
from src.util.read_file import read_dospedia
from src.util.user_input import try_user_choose_from_list


def info_module(event):
    available_characters = get_character_library().keys()
    character_name = try_user_choose_from_list(available_characters)
    character = get_char(character_name)
    modifiers = character.modifiers
    modifier_names = sort_strings_by_length(modifiers.keys())
    dospedia = read_dospedia()
    table_data = []
    for modifier in modifier_names:
        modifier_value = modifiers.get(modifier)
        dospedia_entry = dospedia.get(modifier, 'No entry.')
        full_modifier_name = _build_full_modifier_name(
            modifier, modifier_value)
        row = [full_modifier_name, dospedia_entry]
        table_data.append(row)
    print_table(table_data, character.name, headers=False)
    print_entity_dict(character, SKILLS)
    print_entity_dict(character, CHARACTERISTICS)
    return event


def _build_full_modifier_name(modifier_name, modifier_value):
    if modifier_value is True:
        full_modifier_name = modifier_name
    else:
        full_modifier_name = modifier_name + '(%s)' % modifier_value
    return full_modifier_name
