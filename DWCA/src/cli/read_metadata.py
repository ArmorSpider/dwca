from definitions import RAW_WEAPON_STATS, NUM_HITS, EFFECTIVE_PSY_RATING,\
    BLOCKED, EFFECTIVE_TOUGHNESS, EFFECTIVE_ARMOR, EFFECTIVE_DAMAGE, RAW_DAMAGE,\
    ROLLED_DAMAGE, HIT_LOCATIONS, MAGNITUDE_DAMAGE, FIREMODE, WEAPON,\
    DEGREES_OF_SUCCESS, ROLL_RESULT, ROLL_TARGET, TARGET, ATTACKER, JAMMED,\
    RATE_OF_FIRE
from src.cli.table import print_table
from src.dwca_log.log import get_log
from src.entities import FLAT_DAMAGE, DICE, PENETRATION, ARMOR, DAMAGE_TYPE,\
    WOUNDS


LOG = get_log(__name__)


def present_metadata(metadata):
    LOG.info('[RESULTS]')
    log_attack_base_info(metadata)
    log_conditional_info(metadata)
    log_metadata_table(metadata)
    log_total_summary(metadata)


def log_attack_base_info(metadata):
    attacker = metadata.get(ATTACKER)
    target = metadata.get(TARGET)
    roll_target = metadata.get(ROLL_TARGET)
    roll_result = metadata.get(ROLL_RESULT)
    dos = metadata.get(DEGREES_OF_SUCCESS)
    weapon = metadata.get(WEAPON)
    raw_weapon_stats = metadata.get(RAW_WEAPON_STATS, {})
    raw_flat_damage = raw_weapon_stats.get(FLAT_DAMAGE)
    raw_dice = raw_weapon_stats.get(DICE)
    raw_penetration = raw_weapon_stats.get(PENETRATION)
    damage_type = metadata.get(DAMAGE_TYPE)
    firemode = metadata.get(FIREMODE, 'N/A')
    rof = metadata.get(RATE_OF_FIRE, 'N/A')
    num_hits = metadata.get(NUM_HITS, 0)
    LOG.info('%s attacks %s!', attacker, target)
    LOG.info('Rolled %s vs. %s. (%s DoS)', roll_result, roll_target, dos)
    LOG.info('Weapon: %s [%sd10+%s %s Pen: %s]', weapon,
             raw_dice, raw_flat_damage, damage_type, raw_penetration)
    LOG.info('Attack scored %s hit(s)! Firemode: "%s" RoF: %s',
             num_hits, firemode, rof)


def log_conditional_info(metadata):
    effective_psy_rating = metadata.get(EFFECTIVE_PSY_RATING)
    if effective_psy_rating is not None:
        LOG.info('EFFECTIVE PSY RATING: %s', effective_psy_rating)
    jammed = metadata.get(JAMMED)
    if jammed is True:
        LOG.info('ATTACK JAMMED!')


def log_total_summary(metadata):
    effective_damage_list = metadata.get(EFFECTIVE_DAMAGE, [])
    magnitude_damage_list = metadata.get(MAGNITUDE_DAMAGE, [])
    attack_total_damage = sum([int(s_) for s_ in effective_damage_list])
    total_magnitude_damage = sum([int(s_) for s_ in magnitude_damage_list])
    if attack_total_damage > 0:
        LOG.info('ATTACK TOTAL DAMAGE: %s', attack_total_damage)
        max_wounds = metadata.get(WOUNDS, 0)
        current_wounds = max_wounds - attack_total_damage
        LOG.info('TARGET WOUNDS: %s (%s - %s)', current_wounds,
                 max_wounds, attack_total_damage)
    if total_magnitude_damage > 0:
        LOG.info('TOTAL MAGNITUDE DAMAGE: %s', total_magnitude_damage)


def log_metadata_table(metadata):
    rolled_damage_list = metadata.get(ROLLED_DAMAGE, [])
    raw_damage_list = metadata.get(RAW_DAMAGE, [])
    effective_damage_list = metadata.get(EFFECTIVE_DAMAGE, [])
    effective_armor_list = metadata.get(EFFECTIVE_ARMOR, [])
    effective_toughness_list = metadata.get(EFFECTIVE_TOUGHNESS, [])
    blocked_list = metadata.get(BLOCKED, [])
    hit_locs_list = metadata.get(HIT_LOCATIONS, [])
    magnitude_damage_list = metadata.get(MAGNITUDE_DAMAGE, [])
    flat_damage = metadata.get(FLAT_DAMAGE)
    penetration = metadata.get(PENETRATION)
    num_hits = metadata.get(NUM_HITS, 0)
    armor_dict = metadata.get(ARMOR)

    table_data = [['HIT',
                   'EFFECTIVE_DAMAGE',
                   'RAW DAMAGE',
                   'ARMOR',
                   'BLOCKED',
                   'MAGNITUDE']]
    for hit_information in zip(list(range(1, num_hits + 1)),
                               rolled_damage_list,
                               raw_damage_list,
                               effective_armor_list,
                               effective_toughness_list,
                               effective_damage_list,
                               hit_locs_list,
                               blocked_list,
                               magnitude_damage_list):

        row = build_row(hit_information, armor_dict, flat_damage, penetration)
        table_data.append(row)
    if len(table_data) > 1:
        print_table(table_data, 'ATTACK')


def build_row(hit_information, armor_dict, flat_damage, penetration):
    def get_armor(hit_location):
        armor = armor_dict.get(hit_location)
        if armor is None:
            armor = armor_dict.get('all', 0)
        return armor

    hit_number, rolled_damage, raw_damage, effective_armor, effective_toughness, effective_damage, hit_location, block_result, magnitude_damage = hit_information
    raw_armor = get_armor(hit_location)
    raw_damage_entry = '{raw} ({rolled} + {flat})'.format(raw=raw_damage,
                                                          rolled=rolled_damage,
                                                          flat=flat_damage)

    armor_entry_base = '{effective} ({raw} Armor - {pen} Penetration)'
    armor_entry = armor_entry_base.format(effective=effective_armor,
                                          raw=raw_armor,
                                          pen=penetration)

    effective_damage_base = '{effective} ({raw} Raw Damage - {armor} Armor - {toughness} Toughness)'
    effective_damage_cool = effective_damage if effective_damage == 0 else '[{}]'.format(
        effective_damage)
    effective_damage_entry = effective_damage_base.format(effective=effective_damage_cool,
                                                          raw=raw_damage,
                                                          armor=effective_armor,
                                                          toughness=effective_toughness)
    hit_entry = '{num} ({hitloc})'.format(num=hit_number,
                                          hitloc=hit_location)
    blocked_entry = block_result if block_result is True else ''
    magnitude_entry = magnitude_damage
    row = [hit_entry,
           effective_damage_entry,
           raw_damage_entry,
           armor_entry,
           blocked_entry,
           magnitude_entry]
    return row
