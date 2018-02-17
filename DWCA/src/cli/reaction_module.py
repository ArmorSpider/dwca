from definitions import ROLL_RESULT
from src.action.action import try_action
from src.dice import roll_action_dice
from src.dwca_log.log import get_log
from src.handler import build_base_attack,\
    choose_or_build_attacker
from src.modifiers.roll_modifier import get_effective_modifier


LOG = get_log(__name__)


def defensive_action(event):
    defense_test_result = roll_action_dice()
    event[ROLL_RESULT] = defense_test_result
    attempt_dodge(event)
    attempt_parry(event)
    event.pop(ROLL_RESULT)
    return event


def attempt_dodge(event):
    attacker = choose_or_build_attacker(event)
    roll_result = event.get(ROLL_RESULT)
    base_target = attacker.available_skills.get('dodge')
    modifier = get_effective_modifier(event, manual_only=True)
    roll_target = base_target + modifier
    LOG.info('[DODGE TEST]')
    try_action(roll_target, roll_result)


def attempt_parry(event):
    attack = build_base_attack(event)
    roll_result = event.get(ROLL_RESULT)
    parry_target = 0
    if attack.is_melee():
        parry_target = attack.attacker.available_skills.get('parry')
        manual_bonus = get_effective_modifier(event, manual_only=True)
        parry_target += manual_bonus
        if attack.balanced is not None:
            parry_target += 10 if attack.balanced is True else attack.balanced
        if attack.unbalanced is not None:
            parry_target -= 10
        if attack.hunter_of_aliens is not None and attack.target.is_alien():
            parry_target += 10
            LOG.info('+10 to parry against aliens from HunterOfAliens.')
        if attack.slayer_of_daemons is not None and attack.target.is_daemon():
            parry_target += 10
            LOG.info('+10 to parry against daemons from SlayerOfDaemons.')
        if attack.unwieldy is not None:
            parry_target = 0
            LOG.info('Parry not possible with Unwieldy weapon.')
    if parry_target != 0:
        LOG.info('[PARRY TEST] (%s)', attack.weapon.name)
        try_action(parry_target, roll_result)
