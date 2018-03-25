
import unittest

from definitions import ATTACKER, WEAPON, TARGET, ROLL_TARGET, ROLL_RESULT,\
    DEGREES_OF_SUCCESS, NUM_HITS, ROLLED_DAMAGE, RAW_DAMAGE,\
    OFFENSIVE_MODIFIERS, AD_HOC, DEFENSIVE_MODIFIERS, FIREMODE, EFFECTIVE_DAMAGE,\
    HIT_LOCATIONS, RAW_WEAPON_STATS, EFFECTIVE_ARMOR, EFFECTIVE_TOUGHNESS,\
    EFFECTIVE_PSY_RATING, JAMMED, RATE_OF_FIRE
from src.cli.commands import process_command
from src.dice import queue_d100_rolls, queue_d10_rolls
from src.entities import DICE,\
    FLAT_DAMAGE, PENETRATION, SINGLE_SHOT, TEARING_DICE, FULL_AUTO, DAMAGE_TYPE,\
    ARMOR, WOUNDS
from src.entities.char_stats import STAT_AGI, STAT_STR, STAT_TGH, STAT_WS,\
    STAT_BS
from src.handler import build_attack
from src.hit_location import HITLOC_LEFT_LEG, HITLOC_RIGHT_LEG, HITLOC_BODY, HITLOC_RIGHT_ARM,\
    HITLOC_LEFT_ARM, HITLOC_HEAD
from src.modifiers.qualities import Tearing, Blast
from src.situational.state_manager import StateManager
from src.util.dict_util import pretty_print
from test.test_util import add_mock_entity, add_mock_weapon


class Test(unittest.TestCase):

    def setUp(self):
        StateManager.reset()
        self.automan_name = add_mock_entity('Automan',
                                            traits={'power_armour': True,
                                                    'unnatural_toughness': 2,
                                                    'unnatural_strength': 2},
                                            characteristics={STAT_STR: 40,
                                                             STAT_TGH: 54,
                                                             STAT_WS: 50,
                                                             STAT_BS: 50,
                                                             STAT_AGI: 40},
                                            _system='deathwatch')
        self.dummyman_name = add_mock_entity('Dummyman',
                                             traits={'natural_armor': True},
                                             _system='deathwatch',
                                             wounds=122)
        self.psyman_name = add_mock_entity('Psyman',
                                           traits={'psy_rating': 6},
                                           _system='deathwatch')
        self.armorman_name = add_mock_entity('Armorman',
                                             armor={HITLOC_LEFT_LEG: 11,
                                                    HITLOC_RIGHT_LEG: 12,
                                                    HITLOC_BODY: 13,
                                                    HITLOC_RIGHT_ARM: 14,
                                                    HITLOC_LEFT_ARM: 15,
                                                    HITLOC_HEAD: 16},
                                             characteristics={STAT_TGH: 10},
                                             traits={'daemonic': True,
                                                     'unnatural_toughness': 2},
                                             _system='deathwatch')
        self.business_gun_name = add_mock_weapon('Business Gun',
                                                 'Basic',
                                                 dice=2,
                                                 flat_damage=10,
                                                 penetration=10,
                                                 single_shot=1,
                                                 semi_auto=3,
                                                 full_auto=5,
                                                 _system='deathwatch')
        self.business_fist_name = add_mock_weapon('Business Fist',
                                                  'Melee',
                                                  damage_type='I',
                                                  dice=1,
                                                  flat_damage=10,
                                                  penetration=10,
                                                  qualities={
                                                      Tearing.name: True},
                                                  _system='deathwatch')
        self.business_psy_name = add_mock_weapon('Business Psy',
                                                 'Psychic',
                                                 damage_type='I',
                                                 dice=1,
                                                 flat_damage=10,
                                                 penetration=10,
                                                 qualities={
                                                     'psychic_scaling': True},
                                                 _system='deathwatch')

        self.basic_melee_event = {ATTACKER: self.automan_name,
                                  WEAPON: self.business_fist_name,
                                  TARGET: self.dummyman_name,
                                  ROLL_TARGET: 100}
        self.basic_psy_event = {ATTACKER: self.psyman_name,
                                WEAPON: self.business_psy_name,
                                TARGET: self.dummyman_name,
                                ROLL_TARGET: 100}
        self.armorman_melee_event = {ATTACKER: self.automan_name,
                                     WEAPON: self.business_fist_name,
                                     TARGET: self.armorman_name,
                                     ROLL_TARGET: 100}
        self.single_shot_event = {ATTACKER: self.automan_name,
                                  WEAPON: self.business_gun_name,
                                  TARGET: self.dummyman_name,
                                  FIREMODE: SINGLE_SHOT,
                                  ROLL_TARGET: 100}
        self.full_auto_event = {ATTACKER: self.automan_name,
                                WEAPON: self.business_gun_name,
                                TARGET: self.dummyman_name,
                                FIREMODE: FULL_AUTO,
                                ROLL_TARGET: 100}
        self.armorman_full_auto_event = {ATTACKER: self.automan_name,
                                         WEAPON: self.business_gun_name,
                                         TARGET: self.armorman_name,
                                         FIREMODE: FULL_AUTO,
                                         ROLL_TARGET: 100}

    def tearDown(self):
        pass

    def test_metadata_minimum_should_contain_attacker_weapon_target_and_roll_target(self):
        event = self.basic_melee_event
        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_target_max_wounds(self):
        event = self.basic_melee_event
        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    WOUNDS: 122}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_roll_result(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_effective_psy_rating(self):
        event = self.basic_psy_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Psyman',
                    WEAPON: 'Business Psy',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    EFFECTIVE_PSY_RATING: 6}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_raw_weapon_stats(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])
        raw_weapon_stats = {DICE: 1,
                            PENETRATION: 10,
                            FLAT_DAMAGE: 10}

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    RAW_WEAPON_STATS: raw_weapon_stats}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_target_raw_armor(self):
        event = self.armorman_melee_event
        queue_d100_rolls([51])
        raw_target_armor = {HITLOC_LEFT_LEG: 11,
                            HITLOC_RIGHT_LEG: 12,
                            HITLOC_BODY: 13,
                            HITLOC_RIGHT_ARM: 14,
                            HITLOC_LEFT_ARM: 15,
                            HITLOC_HEAD: 16}

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Armorman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    ARMOR: raw_target_armor}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_degrees_of_success(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_damage_type(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DAMAGE_TYPE: 'I'}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_firemode(self):
        event = self.full_auto_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    FIREMODE: FULL_AUTO}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_rate_of_fire(self):
        event = self.full_auto_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    FIREMODE: FULL_AUTO,
                    RATE_OF_FIRE: 5}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_jammed_status_when_jammed(self):
        event = self.full_auto_event
        queue_d100_rolls([95])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 95,
                    DEGREES_OF_SUCCESS: -1,
                    FIREMODE: FULL_AUTO,
                    JAMMED: True}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_jammed_status_when_not_jammed(self):
        event = self.full_auto_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    FIREMODE: FULL_AUTO,
                    JAMMED: False}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_penetration(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    PENETRATION: 10}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_flat_damage(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    FLAT_DAMAGE: 20}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_num_dice(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    DICE: 1}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_num_tearing_dice(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    TEARING_DICE: 1}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_num_hits(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    NUM_HITS: 1}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_rolled_damage(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5]]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_total_damage(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5]],
                    FLAT_DAMAGE: 20,
                    RAW_DAMAGE: [25]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_multiple_rolled_and_raw_for_multiple_hits(self):
        event = self.full_auto_event
        queue_d100_rolls([51])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_effective_damage(self):
        event = self.full_auto_event
        queue_d100_rolls([51])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20],
                    EFFECTIVE_DAMAGE: [20, 20, 20, 20, 20]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_hit_locations(self):
        event = self.full_auto_event
        queue_d100_rolls([59])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 59,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20],
                    EFFECTIVE_DAMAGE: [20, 20, 20, 20, 20],
                    HIT_LOCATIONS: [HITLOC_LEFT_LEG,
                                    HITLOC_LEFT_LEG,
                                    HITLOC_BODY,
                                    HITLOC_LEFT_ARM,
                                    HITLOC_HEAD]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_effective_armor(self):
        event = self.armorman_full_auto_event
        queue_d100_rolls([59])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Armorman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 59,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    EFFECTIVE_ARMOR: [1, 1, 3, 5, 6],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20],
                    EFFECTIVE_DAMAGE: [16, 16, 14, 12, 11],
                    HIT_LOCATIONS: [HITLOC_LEFT_LEG,
                                    HITLOC_LEFT_LEG,
                                    HITLOC_BODY,
                                    HITLOC_LEFT_ARM,
                                    HITLOC_HEAD]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_effective_toughness(self):
        event = self.armorman_full_auto_event
        queue_d100_rolls([59])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Armorman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 59,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    EFFECTIVE_TOUGHNESS: [3, 3, 3, 3, 3],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20],
                    EFFECTIVE_DAMAGE: [16, 16, 14, 12, 11],
                    HIT_LOCATIONS: [HITLOC_LEFT_LEG,
                                    HITLOC_LEFT_LEG,
                                    HITLOC_BODY,
                                    HITLOC_LEFT_ARM,
                                    HITLOC_HEAD]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_offensive_modifiers(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    OFFENSIVE_MODIFIERS: {'power_armour': True,
                                          'unnatural_strength': 4,
                                          'unnatural_toughness': 5,
                                          Tearing.name: True}}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_defensive_modifiers(self):
        event = self.basic_melee_event
        queue_d100_rolls([51])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    DEFENSIVE_MODIFIERS: {'natural_armor': True}}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_offensive_modifiers_should_include_ad_hoc_mods(self):
        event = self.basic_melee_event
        event[AD_HOC] = {Blast.name: 5}
        queue_d100_rolls([51])
        queue_d10_rolls([5] * 10)

        # This will look for translated values.
        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 51,
                    DEGREES_OF_SUCCESS: 5,
                    OFFENSIVE_MODIFIERS: {'power_armour': True,
                                          'unnatural_strength': 4,
                                          'unnatural_toughness': 5,
                                          Tearing.name: True,
                                          Blast.name: 5}}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def run_cli_commands(self, command_strings):
        event = {}
        for command_string in command_strings:
            event = process_command(command_string, event)
        return event

    def get_attack_metadata(self, event):
        attack = build_attack(event)
        attack.apply_attack()
        attack_metadata = attack.metadata
        pretty_print(attack_metadata)
        return attack_metadata

    def assert_dict_contains(self, expected, actual):
        for key, value in expected.iteritems():
            self.assertEqual(value, actual[key])
