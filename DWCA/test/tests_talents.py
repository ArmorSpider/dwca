import unittest

from src.action.attack import Attack
from src.entities.char_stats import STAT_INT
from src.entities.horde import Horde
from src.modifiers.talents import SlaughterTheSwarm
from test.test_util import build_mock_entity


class Test(unittest.TestCase):

    def test_slaughter_the_swarm(self):
        attacker = build_mock_entity('MockMan',
                                     _system='deathwatch',
                                     characteristics={STAT_INT: 50,
                                                      STAT_INT + '_bonus': 15},
                                     traits={'unnatural_intelligence': 2})
        weapon = None
        target = Horde()
        attack = Attack(weapon, attacker, target)
        current = 10

        expected = 21
        actual = SlaughterTheSwarm().modify_num_hits(attack, current)

        self.assertEqual(expected, actual)
