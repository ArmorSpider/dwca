from itertools import islice, repeat, chain


def build_repeating_iterator(object_):
    return repeat(object_)


def combine_iterators(*iterators):
    return chain(*iterators)


def extract_list_from_iterable(num_objects, iterable):
    return list(islice(iterable, num_objects))
