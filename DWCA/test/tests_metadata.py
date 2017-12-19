
import unittest

from definitions import ATTACKER, WEAPON, TARGET, ROLL_TARGET, ROLL_RESULT,\
    DEGREES_OF_SUCCESS, WEAPONS, CLASS, NUM_HITS, ROLLED_DAMAGE, RAW_DAMAGE,\
    OFFENSIVE_MODIFIERS, AD_HOC, DEFENSIVE_MODIFIERS, FIREMODE, EFFECTIVE_DAMAGE,\
    HIT_LOCATIONS
from src.cli.commands import process_command
from src.dice import queue_d100_rolls, queue_d10_rolls
from src.entities import NAME, TRAITS, CHARACTERISTICS, DAMAGE_TYPE, DICE,\
    FLAT_DAMAGE, PENETRATION, SINGLE_SHOT, TEARING_DICE, QUALITIES, SEMI_AUTO,\
    FULL_AUTO
from src.entities.char_stats import STAT_AGI, STAT_STR, STAT_TGH, STAT_WS,\
    STAT_BS
from src.entities.libraries import MasterLibrary
from src.handler import construct_attack
from src.modifiers.qualities import Tearing, Blast
from src.situational.state_manager import StateManager
from src.util.dict_util import pretty_print


class Test(unittest.TestCase):

    def setUp(self):
        StateManager.reset()
        self.automan_def = {NAME: 'Automan',
                            TRAITS: {'power_armour': True,
                                     'unnatural_toughness': 2,
                                     'unnatural_strength': 2},
                            WEAPONS: ['boltgun'],
                            CHARACTERISTICS: {STAT_STR: 40,
                                              STAT_TGH: 54,
                                              STAT_WS: 50,
                                              STAT_BS: 50,
                                              STAT_AGI: 40}}
        self.dummyman_def = {NAME: 'Dummyman',
                             TRAITS: {'natural_armor': True},
                             WEAPONS: [],
                             CHARACTERISTICS: {}}
        MasterLibrary.add_character('automan', self.automan_def)
        MasterLibrary.add_character('dummyman', self.dummyman_def)
        self.business_gun_def = {NAME: 'Business Gun',
                                 CLASS: 'Basic',
                                 DAMAGE_TYPE: 'I',
                                 DICE: 2,
                                 FLAT_DAMAGE: 10,
                                 PENETRATION: 10,
                                 SINGLE_SHOT: 1,
                                 SEMI_AUTO: 3,
                                 FULL_AUTO: 5}
        self.business_fist_def = {NAME: 'Business Fist',
                                  CLASS: 'Melee',
                                  DAMAGE_TYPE: 'I',
                                  DICE: 1,
                                  FLAT_DAMAGE: 10,
                                  PENETRATION: 10,
                                  QUALITIES: {Tearing.name: True}}
        MasterLibrary.add_weapon('business_gun', self.business_gun_def)
        MasterLibrary.add_weapon('business_fist', self.business_fist_def)
        self.basic_melee_event = {ATTACKER: 'automan',
                                  WEAPON: 'business_fist',
                                  TARGET: 'dummyman',
                                  ROLL_TARGET: 100}
        self.single_shot_event = {ATTACKER: 'automan',
                                  WEAPON: 'business_gun',
                                  TARGET: 'dummyman',
                                  FIREMODE: SINGLE_SHOT,
                                  ROLL_TARGET: 100}
        self.full_auto_event = {ATTACKER: 'automan',
                                WEAPON: 'business_gun',
                                TARGET: 'dummyman',
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

    def test_metadata_should_contain_roll_result(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_degrees_of_success(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_firemode(self):
        event = self.full_auto_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    FIREMODE: FULL_AUTO}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_penetration(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    PENETRATION: 10}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_flat_damage(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    FLAT_DAMAGE: 20}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_num_dice(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    DICE: 1}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_num_tearing_dice(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    TEARING_DICE: 1}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_num_hits(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    NUM_HITS: 1}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_rolled_damage(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5]]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_total_damage(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5]],
                    FLAT_DAMAGE: 20,
                    RAW_DAMAGE: [25]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_multiple_rolled_and_raw_for_multiple_hits(self):
        event = self.full_auto_event
        queue_d100_rolls([50])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_effective_damage(self):
        event = self.full_auto_event
        queue_d100_rolls([50])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20],
                    EFFECTIVE_DAMAGE: [20, 20, 20, 20, 20]}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_hit_locations(self):
        event = self.full_auto_event
        queue_d100_rolls([49])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Gun',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 49,
                    DEGREES_OF_SUCCESS: 5,
                    ROLLED_DAMAGE: [[5, 5], [5, 5], [5, 5], [5, 5], [5, 5]],
                    FLAT_DAMAGE: 10,
                    RAW_DAMAGE: [20, 20, 20, 20, 20],
                    EFFECTIVE_DAMAGE: [20, 20, 20, 20, 20],
                    HIT_LOCATIONS: ['HitLocation.LEFT_LEG',
                                    'HitLocation.LEFT_LEG',
                                    'HitLocation.BODY',
                                    'HitLocation.LEFT_ARM',
                                    'HitLocation.HEAD']}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_offensive_modifiers(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    OFFENSIVE_MODIFIERS: {'power_armour': True,
                                          'unnatural_strength': 2,
                                          'unnatural_toughness': 2,
                                          Tearing.name: True}}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_should_contain_defensive_modifiers(self):
        event = self.basic_melee_event
        queue_d100_rolls([50])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    DEFENSIVE_MODIFIERS: {'natural_armor': True}}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

    def test_metadata_offensive_modifiers_should_include_ad_hoc_mods(self):
        event = self.basic_melee_event
        event[AD_HOC] = {Blast.name: 5}
        queue_d100_rolls([50])
        queue_d10_rolls([5] * 10)

        expected = {ATTACKER: 'Automan',
                    WEAPON: 'Business Fist',
                    TARGET: 'Dummyman',
                    ROLL_TARGET: 100,
                    ROLL_RESULT: 50,
                    DEGREES_OF_SUCCESS: 5,
                    OFFENSIVE_MODIFIERS: {'power_armour': True,
                                          'unnatural_strength': 2,
                                          'unnatural_toughness': 2,
                                          Tearing.name: True,
                                          Blast.name: 5}}
        actual = self.get_attack_metadata(event)
        self.assert_dict_contains(expected, actual)

#     def test_metadata_should_contain_modifier_trigger(self):
#         event = self.basic_melee_event
#         event[AD_HOC] = {Blast.name: 5}
#         queue_d100_rolls([50])
#         queue_d10_rolls([5] * 10)
#
#         expected = {ATTACKER: 'Automan',
#                     WEAPON: 'Business Fist',
#                     TARGET: 'Dummyman',
#                     ROLL_TARGET: 100,
#                     ROLL_RESULT: 50,
#                     DEGREES_OF_SUCCESS: 5,
#                     MODIFIER_EFFECTS: {PowerArmour.name: PowerArmour.message}
#                     }
#         actual = self.get_attack_metadata(event)
#         self.assert_dict_contains(expected, actual)

    def run_cli_commands(self, command_strings):
        event = {}
        for command_string in command_strings:
            event = process_command(command_string, event)
        return event

    def get_attack_metadata(self, event):
        attack = construct_attack(event)
        attack.apply_attack()
        attack_metadata = attack.metadata
        pretty_print(attack_metadata)
        return attack_metadata

    def assert_dict_contains(self, expected, actual):
        for key, value in expected.iteritems():
            self.assertEqual(value, actual[key])
