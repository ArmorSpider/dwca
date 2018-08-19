from mock.mock import patch

from definitions import CLASS, ATTACKER, WEAPON, TARGET
from src.handler import build_attack
from src.util.dict_util import pretty_print
from test.test_util import add_mock_entity, add_mock_weapon


def simulate_attack(event, die_rolls, attacker_def=None, weapon_def=None, target_def=None):
    if attacker_def is None:
        attacker_def = {}
    if weapon_def is None:
        weapon_def = {}
    if target_def is None:
        target_def = {}
    attacker_name = add_mock_entity('ATTACKER', **attacker_def)
    weapon_name = add_mock_weapon(
        'WEAPON', weapon_def.pop(CLASS, 'Melee'), **weapon_def)
    target_name = add_mock_entity('TARGET', **target_def)

    event[ATTACKER] = attacker_name
    event[WEAPON] = weapon_name
    event[TARGET] = target_name

    with patch('src.dice.roll_die', side_effect=die_rolls):
        metadata = get_attack_metadata(event)
    return metadata


def get_attack_metadata(event):
    attack = build_attack(event)
    attack.apply_attack()
    attack_metadata = attack.metadata
    pretty_print(attack_metadata)
    return attack_metadata
