from definitions import WEAPONS, CLASS
from src.entities import SPECIES, SKILLS, TALENTS, NAME, TRAITS, CHARACTERISTICS,\
    WOUNDS, SINGLE_SHOT, SEMI_AUTO, FULL_AUTO, DAMAGE_TYPE, DICE, FLAT_DAMAGE,\
    PENETRATION, QUALITIES
from src.entities.entity_factory import build_entity, build_weapon
from src.entities.libraries import MasterLibrary
from src.util.dict_util import pretty_print
from src.util.rand_util import get_random_string


def build_mock_entity(entity_name, **kwargs):
    entity_hash = add_mock_entity(entity_name, **kwargs)
    entity = build_entity(entity_hash)
    return entity


def add_mock_entity(entity_name, **kwargs):
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


def build_mock_weapon(weapon_name, weapon_class, **kwargs):
    entity_hash = add_mock_weapon(weapon_name, weapon_class, **kwargs)
    entity = build_weapon(entity_hash)
    return entity


def add_mock_weapon(weapon_name, weapon_class, **kwargs):
    definition_name = get_random_string()
    base_definition = {NAME: weapon_name,
                       CLASS: weapon_class,
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
