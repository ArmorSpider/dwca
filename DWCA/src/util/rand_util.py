from random import choice, randint


def select_randomly(choices):
    return choice(choices)


def _random_int(min_, max_):
    return randint(min_, max_)


def roll_die(sides):
    return _random_int(1, sides)
