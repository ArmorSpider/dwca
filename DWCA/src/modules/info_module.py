from src import RULESET
from src.cli.table import print_table
from src.handler import choose_or_build_attacker
from src.util.dict_util import sort_strings_by_length
from src.util.read_file import read_dospedia


def handler_info(event):
    character = choose_or_build_attacker(event)
    modifiers = character.modifiers
    modifier_names = sort_strings_by_length(list(modifiers.keys()))
    dospedia = read_dospedia()
    table_data = []
    for modifier in modifier_names:
        modifier_value = modifiers.get(modifier)
        dospedia_entry = dospedia.get(modifier, "No entry.")
        if isinstance(dospedia_entry, dict):
            dospedia_entry = dospedia_entry[RULESET]
        full_modifier_name = _build_full_modifier_name(modifier, modifier_value)
        row = [full_modifier_name, dospedia_entry]
        table_data.append(row)
    print_table(table_data, character.name, headers=False)
    return event


def _build_full_modifier_name(modifier_name, modifier_value):
    if modifier_value is True:
        full_modifier_name = modifier_name
    else:
        full_modifier_name = f"{modifier_name}({modifier_value})"
    return full_modifier_name
