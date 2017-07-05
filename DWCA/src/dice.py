from src.util.rand_util import roll_die


def roll_action_dice():
    return roll_die(100)


def roll_damage_dice(num_dice):
    results = []
    for _ in range(num_dice):
        result = roll_die(10)
        results.append(result)
    return results
