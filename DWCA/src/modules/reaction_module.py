from definitions import ROLL_RESULT, WEAPON
from src.action.action import try_action
from src.dice import roll_action_dice
from src.dwca_log.log import get_log
from src.entities.char_stats import STAT_WS
from src.entities.entity_factory import build_weapon
from src.handler import build_base_attack,\
    choose_or_build_attacker, build_attacker
from src.modifiers.roll_modifier import get_effective_modifier
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def handler_defend(event):
    defense_test_result = roll_action_dice()
    event[ROLL_RESULT] = defense_test_result
    attacker = choose_or_build_attacker(event)
    melee_weapons = []
    for weapon_name in attacker.weapons:
        weapon = build_weapon(weapon_name)
        if weapon.is_melee() is True:
            melee_weapons.append(weapon_name)
    if melee_weapons != []:
        weapon_name = try_user_choose_from_list(melee_weapons)
        event[WEAPON] = weapon_name
    if attacker.is_vehicle():
        attempt_vehicle_dodge(event)
        attempt_parry(event)
    else:
        attempt_dodge(event)
        attempt_parry(event)
    event.pop(ROLL_RESULT)
    return event


def attempt_vehicle_dodge(event):
    attacker = build_attacker(event)
    base_target = attacker.available_skills.get('drive', 0)
    modifier = get_effective_modifier(event, manual_only=True)
    size_modifier = -attacker.size_bonus
    manouverability = attacker.manouverability
    roll_result = event.get(ROLL_RESULT)
    roll_target = base_target + modifier + size_modifier + manouverability
    LOG.info('[DODGE TEST]')
    try_action(roll_target, roll_result)


def attempt_dodge(event):
    attacker = build_attacker(event)
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
        parry_target = attack.get_effective_characteristic(STAT_WS)
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
