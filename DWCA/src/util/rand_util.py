from random import choice, randint
import string


def select_randomly(choices):
    return choice(choices)


def _random_int(min_, max_):
    return randint(min_, max_)


def roll_die(sides):
    return _random_int(1, sides)


def get_tens(number):
    return int((number) / 10)


def get_random_string(length=6):
    return ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(length))
