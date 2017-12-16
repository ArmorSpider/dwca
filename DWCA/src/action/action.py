from definitions import ROLL_RESULT, ROLL_TARGET, DEGREES_OF_SUCCESS,\
    MODIFIER_EFFECTS
from src.dice import roll_action_dice
from src.dwca_log.log import get_log
from src.hit_location import get_hit_location
from src.util.rand_util import get_tens
from src.util.string_util import reverse_string


LOG = get_log(__name__)


class Action(object):

    def __init__(self):
        self.roll_result = None
        self.roll_target = None
        self.metadata = {}

    def try_action(self, roll_target, roll_result=None):
        if roll_result is None:
            roll_result = roll_action_dice()
        self.roll_result = int(roll_result)
        self.roll_target = int(roll_target)
        LOG.info('Action has %s DoS. (%s vs. %s).', self.degrees_of_success,
                 self.roll_result, self.roll_target)
        self._update_metadata({ROLL_RESULT: roll_result,
                               ROLL_TARGET: roll_target,
                               DEGREES_OF_SUCCESS: self.degrees_of_success})

    def is_successfull(self):
        result = self.roll_result <= self.roll_target
        LOG.debug('Is roll_result %s vs %s successful: %s',
                  self.roll_result, self.roll_target, result)
        return result

    @property
    def degrees_of_success(self):
        if self.is_successfull() is True:
            dos = get_tens(self.roll_target - self.roll_result)
        else:
            dos = -1
        LOG.debug('Action has %s DoS', dos)
        return dos

    def get_reverse(self):
        roll_string = str(self.roll_result)
        reversed_string = reverse_string(roll_string)
        if len(reversed_string) == 1:
            reversed_string += '0'
        return int(reversed_string)

    def get_hit_location(self):
        reversed_roll = self.get_reverse()
        hit_location = get_hit_location(reversed_roll)
        return hit_location

    def _update_metadata(self, dict_):
        self.metadata.update(dict_)

    def _append_to_metadata(self, metadata_key, value):
        current_list = self.metadata.get(metadata_key, [])
        current_list.append(value)
        self.metadata[metadata_key] = current_list

    def add_modifier_effect_to_metadata(self, key, value):
        current_effects = self.metadata.get(MODIFIER_EFFECTS, {})
        current_effects[key] = value
        self.metadata[MODIFIER_EFFECTS] = current_effects
