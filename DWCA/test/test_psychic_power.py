import unittest

from src.action.psychic_attack import PsychicAttack
from src.entities.entity_factory import build_entity
from src.entities.weapon import get_weapon
from test.test_util import add_mock_weapon, add_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        self.psy_weapon_name = add_mock_weapon('PsyPower', 'Psychic')
        self.psy_weapon = get_weapon(self.psy_weapon_name)
        self.mock_man_name = add_mock_entity('MockMan')
        self.mock_man = build_entity(self.mock_man_name)

    def test_is_psychic_should_return_true_for_class_psychic(self):
        self.assertTrue(self.psy_weapon.is_psychic())

    def test_attacking_with_psychic_weapon_should_create_psychic_attack(self):
        attack = self.mock_man.attack(self.psy_weapon)
        self.assertIsInstance(attack, PsychicAttack,
                              'Attack was not PsychicAttack')
