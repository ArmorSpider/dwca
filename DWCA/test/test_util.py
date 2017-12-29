from definitions import WEAPONS, CLASS
from src.entities import SPECIES, SKILLS, TALENTS, NAME, TRAITS, CHARACTERISTICS,\
    WOUNDS, SINGLE_SHOT, SEMI_AUTO, FULL_AUTO, DAMAGE_TYPE, DICE, FLAT_DAMAGE,\
    PENETRATION, QUALITIES
from src.entities.libraries import MasterLibrary
from src.util.dict_util import pretty_print
from src.util.rand_util import get_random_string


def load_mock_entity(entity_name, **kwargs):
    definition_name = get_random_string()
    base_definition = {NAME: entity_name,
                       TALENTS: {},
                       TRAITS: {},
                       WEAPONS: [],
                       CHARACTERISTICS: {},
                       SPECIES: '',
                       SKILLS: {},
                       WOUNDS: 0}
    base_definition.update(kwargs)
    MasterLibrary.add_character(definition_name, base_definition)
    pretty_print(base_definition)
    return definition_name


def load_mock_weapon(weapon_name, is_melee, **kwargs):
    definition_name = get_random_string()
    base_definition = {NAME: weapon_name,
                       CLASS: 'Melee' if is_melee else 'Basic',
                       DAMAGE_TYPE: 'I',
                       DICE: 1,
                       FLAT_DAMAGE: 10,
                       PENETRATION: 10,
                       QUALITIES: {},
                       SINGLE_SHOT: 1,
                       SEMI_AUTO: 3,
                       FULL_AUTO: 5}
    base_definition.update(kwargs)
    MasterLibrary.add_weapon(definition_name, base_definition)
    return definition_name
