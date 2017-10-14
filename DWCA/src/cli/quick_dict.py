from src.dwca_log.log import get_log
from src.entities.libraries import find_best_match
from src.errors import NoMatchError
from src.util.string_util import normalize_string


LOG = get_log(__name__)

PAIR_SEPARATOR = ','
KEY_VALUE_SEPARATOR = ':'


def quick_dict(input_string, match_map=None):
    pairs = input_string.split(PAIR_SEPARATOR)
    output_dict = {}
    for pair_string in pairs:
        try:
            key, value = parse_pair(pair_string)
        except SyntaxError:
            LOG.warn('Skipping incorrect pair string "%s".', pair_string)
        else:
            key, value = match_pair(key, value, match_map)
            output_dict[key] = value
    return output_dict


def parse_pair(pair_string):
    if is_valid_pair_string(pair_string):
        key, value = (normalize_string(string_)
                      for string_ in pair_string.split(KEY_VALUE_SEPARATOR))
        return key, value
    else:
        raise SyntaxError('Pair string "%s"' % pair_string)


def match_pair(key, value, match_map):
    try:
        possible_keys = match_map.keys()
        key = find_best_match(input_string=key,
                              options=possible_keys)
        possible_values = match_map[key]
        value = find_best_match(input_string=value,
                                options=possible_values)
        return key, value
    except (NoMatchError, AttributeError):
        return key, value


def is_valid_pair_string(pair_string):
    return pair_string.count(KEY_VALUE_SEPARATOR) == 1