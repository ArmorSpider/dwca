from src.dice import roll_action_dice
from src.dwca_log.log import get_log
from src.entities import TRAITS, TALENTS, QUALITIES, DICE, PENETRATION, DAMAGE


LOG = get_log(__name__)


def reverse_string(string_):
    return string_[::-1]


class Action(object):

    def __init__(self):
        self.roll_result = None
        self.roll_target = None

    def try_action(self, roll_target, roll_result=None):
        if roll_result is None:
            roll_result = roll_action_dice()
        self.roll_result = roll_result
        self.roll_target = roll_target

    def is_successfull(self):
        result = self.roll_result <= self.roll_target
        LOG.debug('Is roll_result {} vs {} successfull: {}'.format(
            self.roll_result, self.roll_target, result))
        return result

    def get_degrees_of_success(self):
        if self.is_successfull() is True:
            dos = int((self.roll_target - self.roll_result) / 10)
        else:
            dos = 0
        LOG.debug('GoalRoll has {} DoS'.format(dos))
        return dos

    def get_reverse(self):
        roll_string = str(self.roll_result)
        reversed_string = reverse_string(roll_string)
        if len(reversed_string) == 1:
            reversed_string += '0'
        return int(reversed_string)


class Attack(object):

    def __init__(self, weapon, attacker=None):
        self.weapon = weapon
        self.attacker = attacker

    def get_weapon(self):
        return self.weapon

    def get_attacker(self):
        return self.attacker

    def calculate_num_dice(self):
        num_dice = self._get_weapon_stat(DICE)
        # TODO: Calculate modifiers!
        return num_dice

    def calculate_penetration(self):
        penetration = self._get_weapon_stat(PENETRATION)
        # TODO: Calculate modifiers!
        # razor sharp
        return penetration

    def calculate_flat_damage(self):
        flat_damage = self._get_weapon_stat(DAMAGE)
        # TODO: Calculate modifiers!
        # Str bonus if melee
        return flat_damage

    def _get_attacker_stat(self, stat_name):
        attacker = self.get_attacker()
        stat = attacker.get_stat(stat_name)
        return stat

    def _get_weapon_stat(self, stat_name):
        weapon = self.get_weapon()
        stat = weapon.get_stat(stat_name)
        return stat

    def get_weapon_qualities(self):
        return self._get_weapon_stat(QUALITIES)

    def get_attacker_traits(self):
        return self._get_attacker_stat(TRAITS)

    def get_attacker_talents(self):
        return self._get_attacker_stat(TALENTS)
