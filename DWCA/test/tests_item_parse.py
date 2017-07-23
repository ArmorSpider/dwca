'''
Created on 7 Jul 2017

@author: Dos'
'''
import unittest
from src.item_parse import read_weapon_lines_file


class Test(unittest.TestCase):

    def DISABLED_testName(self):
        expected = self.cool_dict
        actual = read_weapon_lines_file()

        self.assertEqual(expected, actual)

    def setUp(self):
        self.maxDiff = None
        self.cool_dict = {
            "omnissian_axe_(astartespattern)": {
                "dice": 1,
                "flat_damage": 11,
                "penetration": 6,
                "damage_type": "E",
                "qualities": {
                    "power field": True,
                    "unbalanced": True
                },
                "class": "Melee",
                "name": "Omnissian Axe (AstartesPattern)"
            },
            "astartes_chainsword": {
                "dice": 1,
                "flat_damage": 3,
                "penetration": 3,
                "damage_type": "R",
                "qualities": {
                    "balanced": True,
                    "tearing": True
                },
                "class": "Melee",
                "name": "Astartes Chainsword"
            },
            "breaching_augur": {
                "dice": 2,
                "flat_damage": 11,
                "penetration": 7,
                "damage_type": "R",
                "qualities": {
                    "tearing": True,
                    "power field": True,
                    "unwieldy": True
                },
                "class": "Melee",
                "name": "Breaching Augur"
            },
            "lash_whip": {
                "dice": 1,
                "flat_damage": 3,
                "penetration": 3,
                "damage_type": "R",
                "qualities": {
                    "flexible": True,
                    "snare": True
                },
                "class": "Melee",
                "name": "Lash Whip"
            },
            "astartes_power_axe": {
                "dice": 1,
                "flat_damage": 8,
                "penetration": 7,
                "damage_type": "E",
                "qualities": {
                    "power field": True,
                    "unbalanced": True
                },
                "class": "Melee",
                "name": "Astartes Power Axe"
            },
            "astartes_power_sword": {
                "dice": 1,
                "flat_damage": 6,
                "penetration": 6,
                "damage_type": "E",
                "qualities": {
                    "balanced": True,
                    "power field": True
                },
                "class": "Melee",
                "name": "Astartes Power Sword"
            },
            "scything_talons": {
                "dice": 1,
                "flat_damage": 2,
                "penetration": 3,
                "damage_type": "R",
                "qualities": {},
                "class": "Melee",
                "name": "Scything Talons"
            },
            "astartes_lightning_claw": {
                "dice": 1,
                "flat_damage": 6,
                "penetration": 8,
                "damage_type": "E",
                "qualities": {
                    "power field": True,
                    "proven": 4
                },
                "class": "Melee",
                "name": "Astartes Lightning Claw"
            },
            "ceremonial_sword": {
                "dice": 1,
                "flat_damage": 3,
                "penetration": 2,
                "damage_type": "R",
                "qualities": {
                    "balanced": True
                },
                "class": "Melee",
                "name": "Ceremonial Sword"
            },
            "bonesword": {
                "dice": 1,
                "flat_damage": 0,
                "penetration": 6,
                "damage_type": "R",
                "qualities": {
                    "drain life": True
                },
                "class": "Melee",
                "name": "Bonesword"
            },
            "astartes_power_spear": {
                "dice": 1,
                "flat_damage": 6,
                "penetration": 7,
                "damage_type": "E",
                "qualities": {
                    "power field": True
                },
                "class": "Melee",
                "name": "Astartes Power Spear"
            },
            "astartes_executioner_axe": {
                "dice": 1,
                "flat_damage": 13,
                "penetration": 8,
                "damage_type": "E",
                "qualities": {
                    "power field": True,
                    "felling": 1,
                    "unwieldy": True
                },
                "class": "Melee",
                "name": "Astartes Executioner Axe"
            },
            "crozius_arcanum": {
                "dice": 1,
                "flat_damage": 7,
                "penetration": 7,
                "damage_type": "E",
                "qualities": {
                    "balanced": True,
                    "power field": True
                },
                "class": "Melee",
                "name": "Crozius Arcanum"
            },
            "astartes_power_fist": {
                "dice": 2,
                "flat_damage": 0,
                "penetration": 9,
                "damage_type": "E",
                "qualities": {
                    "power field": True,
                    "unwieldy": True
                },
                "class": "Melee",
                "name": "Astartes Power Fist"
            },
            "astartes_force_sword": {
                "dice": 1,
                "flat_damage": 2,
                "penetration": 2,
                "damage_type": "R",
                "qualities": {
                    "balanced": True,
                    "special": True
                },
                "class": "Melee",
                "name": "Astartes Force Sword"
            },
            "astartes_power_falchion": {
                "dice": 1,
                "flat_damage": 4,
                "penetration": 6,
                "damage_type": "E",
                "qualities": {
                    "razor sharp": True,
                    "power field": True
                },
                "class": "Melee",
                "name": "Astartes Power Falchion"
            },
            "bulkhead_shears": {
                "dice": 2,
                "flat_damage": 13,
                "penetration": 6,
                "damage_type": "R",
                "qualities": {
                    "tearing": True,
                    "unwieldy": True
                },
                "class": "Melee",
                "name": "Bulkhead Shears"
            },
            "astartes_force_staff": {
                "dice": 1,
                "flat_damage": 1,
                "penetration": 0,
                "damage_type": "I",
                "qualities": {
                    "balanced": True,
                    "special": True
                },
                "class": "Melee",
                "name": "Astartes Force Staff"
            },
            "astartes_thunder_hammer": {
                "dice": 2,
                "flat_damage": 5,
                "penetration": 9,
                "damage_type": "E",
                "qualities": {
                    "power field": True,
                    "concussive": True,
                    "unwieldy": True
                },
                "class": "Melee",
                "name": "Astartes Thunder Hammer"
            },
            "astartes_power_claymore": {
                "dice": 1,
                "flat_damage": 11,
                "penetration": 8,
                "damage_type": "E",
                "qualities": {
                    "devastating": 1,
                    "power field": True,
                    "unwieldy": True
                },
                "class": "Melee",
                "name": "Astartes Power Claymore"
            },
            "astartes_combat_knife": {
                "dice": 1,
                "flat_damage": 0,
                "penetration": 0,
                "damage_type": "R",
                "qualities": {},
                "class": "Melee",
                "name": "Astartes Combat Knife"
            },
            "sacris_claymore": {
                "dice": 2,
                "flat_damage": 2,
                "penetration": 2,
                "damage_type": "R",
                "qualities": {
                    "unbalanced": True
                },
                "class": "Melee",
                "name": "Sacris Claymore"
            },
            "rending_claws": {
                "dice": 1,
                "flat_damage": 0,
                "penetration": 5,
                "damage_type": "R",
                "qualities": {
                    "razor sharp": True
                },
                "class": "Melee",
                "name": "Rending Claws"
            },
            "astartes_chainfist": {
                "dice": 2,
                "flat_damage": 0,
                "penetration": 10,
                "damage_type": "E",
                "qualities": {
                    "tearing": True,
                    "power field": True,
                    "unwieldy": True
                },
                "class": "Mounted",
                "name": "Astartes Chainfist"
            }
        }


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
