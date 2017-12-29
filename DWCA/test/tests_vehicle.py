import unittest
from src.entities import ARMOR, NAME
from src.hit_location import HITLOC_FRONT, HITLOC_SIDE, HITLOC_REAR


class Test(unittest.TestCase):

    def setUp(self):
        self.vehicle_def = {
            ARMOR: {HITLOC_FRONT: 30, HITLOC_SIDE: 20, HITLOC_REAR: 10},
            NAME: 'Cool Car'}

    def tearDown(self):
        pass

    def testName(self):
        pass
