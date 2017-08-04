
import unittest


from src.entities.character import get_char
from src.entities.weapon import get_weapon
from src.modifiers.modifier import register_modifiers

# pylint: skip-file


class Test(unittest.TestCase):

    def setUp(self):
        register_modifiers()

    def test_genestealer(self):
        attacker = get_char('auran_genestealer')
        target = get_char('john_bobb')
        weapon = get_weapon('rending_claws')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(96, 1)
        expected_dice = 1
        expected_pen = 10
        expected_damage = 14
        expected_dos = 9

        actual_dice = attack._get_num_dice()
        actual_pen = attack._get_penetration()
        actual_damage = attack._get_flat_damage()
        actual_dos = attack.get_degrees_of_success()

        self.assertEqual(expected_dice, actual_dice)
        self.assertEqual(expected_pen, actual_pen)
        self.assertEqual(expected_damage, actual_damage)
        self.assertEqual(expected_dos, actual_dos)

    def test_john(self):
        target = get_char('auran_genestealer')
        attacker = get_char('john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        expected = 2
        actual = attack._get_tearing_dice()
        self.assertEqual(expected, actual)

    def test_bohn_roll_to_confirm(self):
        target = get_char('auran_genestealer')
        attacker = get_char('bohn_jobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(50)
        flat_damage = attack._get_flat_damage()
        num_dice = attack._get_num_dice()
        max_damage_without_fury = flat_damage + (num_dice * 10)
        damage = 0
        while damage < max_damage_without_fury:
            damage = attack._roll_damage()
        self.assertTrue(damage >= max_damage_without_fury)

    def test_john_auto_confirm(self):
        target = get_char('auran_genestealer')
        attacker = get_char('john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(0)
        flat_damage = attack._get_flat_damage()
        num_dice = attack._get_num_dice()
        max_damage_without_fury = flat_damage + (num_dice * 10)
        damage = 0
        while damage < max_damage_without_fury:
            damage = attack._roll_damage()
        self.assertTrue(damage >= max_damage_without_fury)

    def test_ayo(self):
        target = get_char('auran_genestealer')
        attacker = get_char('john_bobb')
        weapon = get_weapon('astartes_chainsword')
        attack = attacker.melee_attack(weapon, target)
        attack.try_action(100, 50)
        num_hits = attack._get_num_hits()
        hits = list(attack.hits_generator())
        self.assertTrue(len(hits) == num_hits)
