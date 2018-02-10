from src.dwca_log.log import get_log
from src.entities import CHARACTERISTICS, TRAITS, QUALITIES, SKILLS
from src.entities.char_stats import STAT_TGH
from src.util.rand_util import get_tens


LOG = get_log(__name__)

FELLING_FACTOR = 4


def translate_entity(entity_def):
    entity_def = translate_unnatural_characteristics(entity_def)
    entity_def = translate_entity_traits(entity_def)
    entity_def = translate_skills(entity_def)
    return entity_def


def translate_weapon(weapon_def):
    weapon_def = translate_weapon_qualities(weapon_def)
    return weapon_def


def translate_unnatural_characteristics(entity_def):
    characteristics = entity_def.get(CHARACTERISTICS)
    if characteristics is None:
        LOG.warn(
            'Cannot translate unnatural characteristics. No characteristics defined.')
        return entity_def
    for characteristic in characteristics.keys():
        unnatural_name = 'unnatural_' + characteristic
        traits = entity_def.get(TRAITS, {})
        unnatural_value = traits.get(unnatural_name, None)
        if unnatural_value is None:
            continue
        else:
            characteristic_value = characteristics[characteristic]
            raw_bonus = get_tens(characteristic_value)
            current_bonus = raw_bonus * unnatural_value
            new_unnatural = current_bonus - raw_bonus
            entity_def[TRAITS][unnatural_name] = new_unnatural
            LOG.info('Converted %s from %s to %s',
                     unnatural_name, unnatural_value, new_unnatural)
    return entity_def


def translate_skills(entity_def):
    skills = entity_def.get(SKILLS)
    if skills is None:
        LOG.warn('Cannot translate skills. No skills defined.')
        return entity_def
    if skills.get('parry') is None:
        entity_def[SKILLS]['parry'] = 0
        LOG.info('Added parry skill.')
    if skills.get('carouse') is not None:
        entity_def[SKILLS].pop('carouse', None)
    consolidation_map = {'acrobatics': ['acrobatics', 'contortionist'],
                         'awareness': ['awareness', 'lip_reading', 'search'],
                         'charm': ['charm', 'performer'],
                         'commerce': ['barter', 'commerce'],
                         'logic': ['logic', 'gambling', 'tactics'],
                         'linguistics': ['ciphers', 'literacy', 'secret_tongue', 'speak_language'],
                         'medicae': ['chem_use', 'medicae'],
                         'operate': ['drive', 'pilot'],
                         'stealth': ['concealment', 'silent_move', 'shadowing'],
                         'survival': ['survival', 'tracking', 'wrangling'],
                         'tech_use': ['demolitions', 'tech_use']}
    for core_skill, consolidated_skills in consolidation_map.iteritems():
        skills = _consolidate_skill(core_skill, consolidated_skills, skills)
    return entity_def


def _consolidate_skill(core_skill, consolidated_skills, skills):
    skill_values = []
    for skill in consolidated_skills:
        if skill in skills:
            skill_value = skills.get(skill)
            skill_values.append(skill_value)
            skills.pop(skill, None)
            LOG.info('Consolidated skill %s into %s', skill, core_skill)
    if skill_values != []:
        skills[core_skill] = max(skill_values)
    return skills


def translate_entity_traits(entity_def):
    traits = entity_def.get(TRAITS)
    if traits is None:
        LOG.warn('Cannot translate traits. No traits defined.')
        return entity_def
    if traits.get('daemonic') is True:
        toughness = entity_def[CHARACTERISTICS][STAT_TGH]
        tgh_bonus = get_tens(toughness)
        entity_def[TRAITS]['daemonic'] = tgh_bonus
        LOG.info('Updated daemonic from true to %s', tgh_bonus)
    if traits.get('brutal_charge') is True:
        entity_def[TRAITS]['brutal_charge'] = 3
        LOG.info('Updated brutal_charge from true to 3')
    if traits.get('multiple_arms') is True:
        entity_def[TRAITS]['multiple_arms'] = 4
        LOG.info('Updated multiple_arms from true to 4')
    return entity_def


def translate_weapon_qualities(weapon_def):
    qualities = weapon_def.get(QUALITIES)
    if qualities is None:
        LOG.warn('Cannot translate qualities. No qualities defined.')
        return weapon_def
    if qualities.get('concussive') is True:
        weapon_def[QUALITIES]['concussive'] = 1
        LOG.info('Updated concussive from true to 1')
    if qualities.get('primitive') is True:
        weapon_def[QUALITIES]['primitive'] = 8
        LOG.info('Updated primitive from true to 8')
    if qualities.get('snare') is True:
        weapon_def[QUALITIES]['snare'] = 1
        LOG.info('Updated snare from true to 1')
    if qualities.get('deadly_snare') is True:
        weapon_def[QUALITIES]['deadly_snare'] = 1
        LOG.info('Updated deadly_snare from true to 1')
    if qualities.get('felling') is not None:
        old_felling = qualities.get('felling')
        new_felling = old_felling * FELLING_FACTOR
        weapon_def[QUALITIES]['felling'] = new_felling
        LOG.info('Updated felling from %s to %s', old_felling, new_felling)
    return weapon_def
