from definitions import NUM_ATTACKS
from src.cli.message_queue import log_messages
from src.cli.read_metadata import present_metadata
from src.dwca_log.log import get_log
from src.errors import MechanicsError
from src.handler import build_attack
from src.situational.state_manager import StateManager


LOG = get_log(__name__)


def handler_run(event):
    StateManager.update(event)
    main_handler(event)
    log_messages()
    return event


def main_handler(event):
    attack_damages = multiple_attacks(event)
    raw_damage = sum(attack_damages)
    LOG.info('All attacks combined damage: %s (%s)', raw_damage,
             ' + '.join([str(attack_damage) for attack_damage in attack_damages]))
    return attack_damages


def multiple_attacks(event):
    num_attacks = event.get(NUM_ATTACKS, 1)
    attack_damages = []
    for attack_number in range(int(num_attacks)):
        attack_damage = single_attack(event, attack_number + 1)
        attack_damages.append(attack_damage)
    return attack_damages


def single_attack(event, attack_number):
    LOG.info('________[ATTACK %s]________', attack_number)
    attack = build_attack(event)
    attack_damage = attack.apply_attack()
    try:
        present_metadata(attack.metadata)
    except Exception:
        LOG.exception('')
        raise MechanicsError('Failed presenting metadata.')
    return attack_damage
