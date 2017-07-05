from src.entities.attack import Attack


class Entity(object):

    def __init__(self, definition=None):
        self.definition = definition

    def get_definition(self):
        return self.definition

    def get_stat(self, stat_name):
        return self.get_definition().get(stat_name)


class Character(Entity):

    def attack(self, weapon, target=None):
        return Attack(weapon=weapon,
                      attacker=self,
                      target=target)
