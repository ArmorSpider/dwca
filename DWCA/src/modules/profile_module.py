from src.cli.table import print_table
from src.dwca_log.log import get_log
from src.entities import HALF_MOVE, FULL_MOVE,\
    CHARGE_MOVE, RUN_MOVE
from src.entities.char_stats import STAT_WS, STAT_BS, STAT_STR, STAT_TGH,\
    STAT_AGI, STAT_INT, STAT_PER, STAT_WIL, STAT_FEL
from src.entities.entity_factory import build_weapon
from src.handler import build_attacker
from src.hit_location import HITLOC_BODY
from src.util.dict_util import sort_strings_by_length


LOG = get_log(__name__)


def handler_profile(event):
    attacker = build_attacker(event)
    stats = {'WS': attacker.get_characteristic(STAT_WS),
             'BS': attacker.get_characteristic(STAT_BS),
             'S': attacker.get_characteristic(STAT_STR),
             'T': attacker.get_characteristic(STAT_TGH),
             'Ag': attacker.get_characteristic(STAT_AGI),
             'Int': attacker.get_characteristic(STAT_INT),
             'Per': attacker.get_characteristic(STAT_PER),
             'WP': attacker.get_characteristic(STAT_WIL),
             'Fel': attacker.get_characteristic(STAT_FEL)}

    header_row = []
    stat_row = []
    for stat_name, stat_value in stats.iteritems():
        header_row.append(stat_name)
        stat_row.append(stat_value)
    table_data = [header_row,
                  stat_row]

    print_table(table_data, attacker.name, headers=True)

    move_opts = attacker.movement
    LOG.info('[Movement: %s/%s/%s/%s]',
             move_opts.get(HALF_MOVE),
             move_opts.get(FULL_MOVE),
             move_opts.get(CHARGE_MOVE),
             move_opts.get(RUN_MOVE))

    armor = attacker.get_armor(HITLOC_BODY)
    toughness_bonus = attacker.get_raw_characteristic_bonus(STAT_TGH)
    toughness_multiplier = attacker.get_characteristic_multiplier(STAT_TGH)
    toughness_flat = attacker.get_flat_characteristic_bonus(STAT_TGH)
    toughness_actual = (
        toughness_bonus * toughness_multiplier) + toughness_flat
    LOG.info('[Armor: %s TGH: %s (%s x %s + %s)]', armor, toughness_actual,
             toughness_bonus, toughness_multiplier, toughness_flat)

    LOG.info('[Weapons]')
    weapon_strings = []
    for weapon_name in attacker.weapons:
        weapon = build_weapon(weapon_name)
        dice = weapon.dice
        flat_damage = weapon.flat_damage
        damage_type = weapon.damage_type
        penetration = weapon.penetration
        quality_strings = []
        for quality_name, quality_value in weapon.qualities.iteritems():
            if quality_value is True:
                quality_string = quality_name
            else:
                quality_string = '{}({})'.format(quality_name, quality_value)
            quality_strings.append(quality_string)
        quality_summaries = ', '.join(quality_strings)
        weapon_string = '{} - [{}d10+{} {} Pen: {}; {}]'.format(weapon,
                                                                dice,
                                                                flat_damage,
                                                                damage_type,
                                                                penetration,
                                                                quality_summaries)
        weapon_strings.append(weapon_string)
    for weapon_string in sort_strings_by_length(weapon_strings):
        LOG.info(weapon_string)

    return event
