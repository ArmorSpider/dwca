from src.dwca_log.log import get_log

LOG = get_log(__name__)


def user_input_string(prompt):
    string_ = str(raw_input(prompt))
    return string_


def user_input_int(prompt):
    int_ = int(raw_input(prompt))
    return int_


def ask_user(prompt):
    yn_prompt = prompt + ' (y/n)'
    input_string = user_input_string(yn_prompt)
    result = input_string.lower() == 'y'
    return result


def user_choose_from_list(list_):
    if len(list_) == 1:
        user_choice = list_[0]
    else:
        for index, string_ in enumerate(list_):
            LOG.info('%s: %s', index + 1, string_)
        index = input('Enter a number: (1-%s) ' % len(list_))
        user_choice = list_[index - 1]
    return user_choice
