import unittest

from src.action.attack import Attack
from src.entities.entity_factory import build_entity
from src.modifiers.states import Unfettered, Push, Fettered
from src.modifiers.talents import WarpConduit
from test.test_util import add_mock_entity


class Test(unittest.TestCase):

    def setUp(self):
        self.non_psyker = build_entity(add_mock_entity('Non-psyker'))
        self.psyker = build_entity(add_mock_entity('Pskyer',
                                                   traits={'psy_rating': 3}))
        self.unnatural_psyker = build_entity(add_mock_entity('Pskyer',
                                                             traits={'psy_rating': 3,
                                                                     'unnatural_willpower': 2}))

    def tearDown(self):
        pass

    def test_non_pskyer_psy_rating_should_return_none(self):
        attack = Attack(weapon=None, attacker=self.non_psyker, target=None)
        expected = None
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)

    def test_pskyer_should_return_correct_psy_rating(self):
        attack = Attack(weapon=None, attacker=self.psyker, target=None)
        expected = 3
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)

    def test_unnatural_pskyer_should_not_add_unnatural_multiplier(self):
        attack = Attack(
            weapon=None, attacker=self.unnatural_psyker, target=None)
        expected = 3
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)

    def test_unfettered_should_use_base_psy_rating(self):
        attack = Attack(weapon=None, attacker=self.psyker, target=None)
        attack.ad_hoc_modifiers = {'unfettered': True}
        expected = 3
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)

    def test_push_should_use_base_psy_rating_plus_three(self):
        attack = Attack(weapon=None, attacker=self.psyker, target=None)
        attack.ad_hoc_modifiers = {'push': True}
        expected = 6
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)

    def test_warp_conduit_should_add_one_psy_rating_when_pushing(self):
        attack = Attack(weapon=None, attacker=self.psyker, target=None)
        attack.ad_hoc_modifiers = {'push': True,
                                   'warp_conduit': True}
        expected = 7
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)

    def test_fettered_should_use_half_base_psy_rating_rounded_up(self):
        attack = Attack(weapon=None, attacker=self.psyker, target=None)
        attack.ad_hoc_modifiers = {'fettered': True}
        expected = 2
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)

    def test_fettered_should_work_with_other_modifiers(self):
        attack = Attack(
            weapon=None, attacker=self.unnatural_psyker, target=None)
        attack.ad_hoc_modifiers = {'fettered': True}
        expected = 2
        actual = attack.effective_psy_rating
        self.assertEqual(expected, actual)
