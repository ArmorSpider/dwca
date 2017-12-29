from src.hit_location import HitLocation, HEAD, BODY, LEFT_ARM, RIGHT_ARM,\
    LEFT_LEG, RIGHT_LEG, FRONT, SIDE, REAR
from src.util.iterator_util import build_repeating_iterator, combine_iterators,\
    extract_list_from_iterable
from src.util.rand_util import select_randomly


RANDOM_ARM = 'RANDOM_ARM'


def get_hit_locations(first_hit_location, num_hits):
    hitloc_iterator = build_hitloc_iterator(first_hit_location)
    hit_locations = extract_list_from_iterable(num_hits, hitloc_iterator)
    return hit_locations


def build_hitloc_iterator(hit_location):
    hit_series = get_hit_series(hit_location)
    repeater = build_repeating_iterator(hit_series[-1])
    combined = combine_iterators(hit_series, repeater)
    return combined


def get_hit_series(hit_location):
    master_dict = build_hit_series_dict()
    hit_series = master_dict[hit_location]
    return hit_series


def build_hit_series_dict():
    return {HEAD: build_head_hit_series(),
            BODY: build_body_hit_series(),
            LEFT_ARM: build_left_arm_hit_series(),
            RIGHT_ARM: build_right_arm_hit_series(),
            LEFT_LEG: build_left_leg_hit_series(),
            RIGHT_LEG: build_right_leg_hit_series(),
            FRONT: [FRONT],
            SIDE: [SIDE],
            REAR: [REAR]}


def build_head_hit_series():
    order_string = '112323'
    choice_list = [HEAD, RANDOM_ARM, BODY]
    hit_series = build_hit_series(order_string, choice_list)
    return hit_series


def build_body_hit_series():
    order_string = '112321'
    choice_list = [BODY, RANDOM_ARM, HEAD]
    hit_series = build_hit_series(order_string, choice_list)
    return hit_series


def build_left_arm_hit_series():
    order_string = '112321'
    choice_list = [LEFT_ARM, BODY, HEAD]
    hit_series = build_hit_series(order_string, choice_list)
    return hit_series


def build_right_arm_hit_series():
    order_string = '112321'
    choice_list = [RIGHT_ARM, BODY, HEAD]
    hit_series = build_hit_series(order_string, choice_list)
    return hit_series


def build_left_leg_hit_series():
    order_string = '112342'
    choice_list = [LEFT_LEG, BODY,
                   LEFT_ARM, HEAD]
    hit_series = build_hit_series(order_string, choice_list)
    return hit_series


def build_right_leg_hit_series():
    order_string = '112342'
    choice_list = [RIGHT_LEG, BODY,
                   RIGHT_ARM, HEAD]
    hit_series = build_hit_series(order_string, choice_list)
    return hit_series


def get_random_arm_hitloc():
    return select_randomly([HitLocation.LEFT_ARM, HitLocation.RIGHT_ARM])


def build_hit_series(order_string, choice_list):
    base_list = []
    for choice_index in order_string:
        hit_loc = choice_list[int(choice_index) - 1]
        if hit_loc == RANDOM_ARM:
            hit_loc = get_random_arm_hitloc()
        base_list.append(hit_loc)
    return base_list
