from src.entities.character import Character
from src.util.read_file import read_character


def get_horde(creature_name, magnitude):
    char_definition = read_character(creature_name)
    horde = Horde(char_definition, magnitude)
    return horde


class Horde(Character):

    def __init__(self, definition=None, magnitude=1):
        Character.__init__(self, definition=definition)
        self.magnitude = magnitude

    def is_horde(self):
        return True

    def get_magnitude(self):
        return self.magnitude
