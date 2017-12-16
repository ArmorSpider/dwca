import unittest

from definitions import CLASS
from src.entities import NAME, DAMAGE_TYPE, DICE, DAMAGE, PENETRATION,\
    SINGLE_SHOT, QUALITIES
from src.entities.libraries import MasterLibrary
from src.entities.weapon import get_weapon
from src.modifiers.qualities import Tearing


class Test(unittest.TestCase):

    def setUp(self):
        self.business_gun_def = {NAME: 'Business Gun',
                                 CLASS: 'Basic',
                                 DAMAGE_TYPE: 'I',
                                 DICE: 1,
                                 DAMAGE: 10,
                                 PENETRATION: 10,
                                 SINGLE_SHOT: 1}
        self.business_fist_def = {NAME: 'Business Fist',
                                  CLASS: 'Melee',
                                  DAMAGE_TYPE: 'I',
                                  DICE: 1,
                                  DAMAGE: 10,
                                  PENETRATION: 10,
                                  QUALITIES: {Tearing.name: True,
                                              'cool_weapon': 'Absolutely'}}
        MasterLibrary.add_weapon('business_gun', self.business_gun_def)
        MasterLibrary.add_weapon('business_fist', self.business_fist_def)

    def test_weapon_modifiers_should_include_qualities(self):
        business_fist = get_weapon('business_fist')
        expected = {Tearing.name: True,
                    'cool_weapon': 'Absolutely'}
        actual = business_fist.modifiers
        self.assertEqual(expected, actual)

    def test_get_attribute_should_do_lookup_in_modifiers(self):
        business_fist = get_weapon('business_fist')
        expected = 'Absolutely'
        actual = business_fist.cool_weapon
        self.assertEqual(expected, actual)
