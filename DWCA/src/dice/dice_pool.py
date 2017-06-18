
class DicePool(object):

    def __init__(self, dice_list):
        self.dice_in_pool = dice_list

    def _roll_dice(self):
        results = []
        for dice in self.dice_in_pool:
            dice_result = dice._roll_dice()
            results.append(dice_result)
        return results

    def roll(self):
        dice_results = self._roll_dice()
        results_total = sum(dice_results)
        return results_total
