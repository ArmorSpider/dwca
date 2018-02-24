import unittest

from src.entities import HALF_MOVE, FULL_MOVE, CHARGE_MOVE,\
    RUN_MOVE
from src.entities.char_stats import STAT_AGI
from src.modifiers.talents import Sprint
from src.modifiers.traits import Size, Quadruped, UnnaturalSpeed, JumpPack,\
    BlackCarapace, UnnaturalAgility, PreternaturalSpeed
from test.test_util import build_mock_entity


class Test(unittest.TestCase):

    def test_movement_should_contain_half_full_charge_and_run_move(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 30})

        expected = {HALF_MOVE: 3,
                    FULL_MOVE: 6,
                    CHARGE_MOVE: 9,
                    RUN_MOVE: 18}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_movement_should_be_based_on_agi_mod(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40})

        expected = {HALF_MOVE: 4,
                    FULL_MOVE: 8,
                    CHARGE_MOVE: 12,
                    RUN_MOVE: 24}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_unnatural_agility_should_affect_movement(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={UnnaturalAgility.name: 2})

        expected = {HALF_MOVE: 8,
                    FULL_MOVE: 16,
                    CHARGE_MOVE: 24,
                    RUN_MOVE: 48}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_quadruped_should_double_agi_mod_for_movement(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={Quadruped.name: True})

        expected = {HALF_MOVE: 8,
                    FULL_MOVE: 16,
                    CHARGE_MOVE: 24,
                    RUN_MOVE: 48}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_sprint_should_increase_full_move_and_run_move(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    talents={Sprint.name: True})

        expected = {HALF_MOVE: 4,
                    FULL_MOVE: 12,
                    CHARGE_MOVE: 12,
                    RUN_MOVE: '24/48*'}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_movement_should_get_bonus_from_positive_size(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={Size.name: 20})

        expected = {HALF_MOVE: 6,
                    FULL_MOVE: 12,
                    CHARGE_MOVE: 18,
                    RUN_MOVE: 36}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_black_carapace_should_not_reduce_movement(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={Size.name: 10, BlackCarapace.name: True})

        expected = {HALF_MOVE: 5,
                    FULL_MOVE: 10,
                    CHARGE_MOVE: 15,
                    RUN_MOVE: 30}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_jump_pack_should_double_base_movement(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={Size.name: 20,
                                            JumpPack.name: True})

        expected = {HALF_MOVE: 10,
                    FULL_MOVE: 20,
                    CHARGE_MOVE: 30,
                    RUN_MOVE: 60}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_unnatural_speed_should_do_nothing_because_it_does_not_exist(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={Size.name: 20,
                                            UnnaturalSpeed.name: True})

        expected = {HALF_MOVE: 6,
                    FULL_MOVE: 12,
                    CHARGE_MOVE: 18,
                    RUN_MOVE: 36}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_preternatural_speed_should_double_charge_movement(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={Size.name: 20,
                                            PreternaturalSpeed.name: True})

        expected = {HALF_MOVE: 6,
                    FULL_MOVE: 12,
                    CHARGE_MOVE: 36,
                    RUN_MOVE: 36}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_movement_should_get_penalty_from_negative_size(self):
        moveman = build_mock_entity('Moveman',
                                    _system='deathwatch',
                                    characteristics={STAT_AGI: 40},
                                    traits={Size.name: -20})

        expected = {HALF_MOVE: 2,
                    FULL_MOVE: 4,
                    CHARGE_MOVE: 6,
                    RUN_MOVE: 12}
        actual = moveman.movement
        self.assertEqual(expected, actual)

    def test_vehicle_movement_should_use_tactical_speed(self):
        movevan = build_mock_entity('Movevan',
                                    vehicle=True,
                                    speed=10)

        expected = {HALF_MOVE: 10,
                    FULL_MOVE: 20,
                    CHARGE_MOVE: 20,
                    RUN_MOVE: 20}
        actual = movevan.movement
        self.assertEqual(expected, actual)
