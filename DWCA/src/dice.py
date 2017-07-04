from random import randint


def roll_action_dice():
    return randint(1, 100)


def roll_damage_dice(num_dice):
    results = []
    for _ in range(num_dice):
        result = randint(1, 10)
        results.append(result)
    return results
