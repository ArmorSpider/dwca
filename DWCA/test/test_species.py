import unittest

from src.entities import SPECIES
from src.entities.character import Character
from src.entities.species import Species


class Test(unittest.TestCase):

    def setUp(self):
        self.human = Character({SPECIES: Species.HUMAN.value})
        self.tyranid = Character({SPECIES: Species.TYRANID.value})
        self.ork = Character({SPECIES: Species.ORK.value})
        self.tau = Character({SPECIES: Species.TAU.value})
        self.daemon = Character({SPECIES: Species.DAEMON.value})
        self.eldar = Character({SPECIES: Species.ELDAR.value})
        self.necron = Character({SPECIES: Species.NECRON.value})
        self.xeno = Character({SPECIES: Species.XENO.value})

    def test_non_aliens_should_not_be_identifed_as_aliens(self):
        non_aliens = [self.human, self.daemon, self.necron]

        for character in non_aliens:
            self.assertFalse(character.is_alien())

    def test_aliens_should_be_identifed_as_aliens(self):
        aliens = [self.tyranid, self.ork, self.tau, self.eldar, self.xeno]

        for character in aliens:
            self.assertTrue(character.is_alien())
