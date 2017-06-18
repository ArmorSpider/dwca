from random import randint

DAMAGE_DICE_SIDES = 10


class Dice(object):

    def __init__(self, sides):
        self.sides = sides

    def _roll_dice(self):
        return self._generate_random_int(1, self.sides)

    def _generate_random_int(self, min_, max_):
        return randint(min_, max_)


class DamageDice(Dice):

    def __init__(self):
        Dice.__init__(self, DAMAGE_DICE_SIDES)


class DummyDice(Dice):

    def _roll_dice(self):
        return self.sides
