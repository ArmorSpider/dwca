from src.dwca_log.log import get_log
from src.entities.libraries import find_best_match
from src.errors import NoMatchError
from src.util.string_util import normalize_string


LOG = get_log(__name__)

PAIR_SEPARATOR = ','
KEY_VALUE_SEPARATOR = ':'


def quick_dict_parse(input_string, match_map=None):
    pairs = input_string.split(PAIR_SEPARATOR)
    output_dict = {}
    for key, value in _pair_parser(pairs, match_map):
        value = _try_int_convert(value)
        output_dict[key] = value
    return output_dict


def _try_int_convert(value):
    try:
        value = int(value)
    except ValueError:
        pass
    return value


def _pair_parser(pairs, match_map):
    for pair_string in pairs:
        try:
            key, value = _parse_pair(pair_string)
            if match_map is not None:
                key, value = _match_pair(key, value, match_map)
        except SyntaxError:
            LOG.warn('Skipping incorrect pair string "%s".', pair_string)
        except NoMatchError:
            LOG.warn(
                'Skipping incorrect pair string "%s". No match found.', pair_string)
        else:
            yield key, value


def _parse_pair(pair_string):
    if _is_valid_pair_string(pair_string):
        key, value = (normalize_string(string_)
                      for string_ in pair_string.split(KEY_VALUE_SEPARATOR))
        return key, value
    else:
        raise SyntaxError('Pair string "%s"' % pair_string)


def _match_pair(key, value, match_map):
    possible_keys = list(match_map.keys())
    matched_key = find_best_match(input_string=key,
                                  options=possible_keys)
    possible_values = match_map[matched_key]
    if possible_values is None:
        return matched_key, value
    matched_value = find_best_match(input_string=value,
                                    options=possible_values)
    return matched_key, matched_value


def _is_valid_pair_string(pair_string):
    return pair_string.count(KEY_VALUE_SEPARATOR) == 1
