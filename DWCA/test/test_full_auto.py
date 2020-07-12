from pprint import pprint
from random import randint, choice


from src.cli.commands import process_command
from src.entities.libraries import MasterLibrary
from src.errors import OutOfRangeError
from src.modules.new_module import handler_new
from src.util.rand_util import _random_int


def return_random(list_):
    thing = choice(list_)
    print(f'Chose "{thing}"')
    return thing


def return_number(prompt):
    return _random_int(1, 100)


def test_run_random_attacks(mocker):
    MasterLibrary.reload_libraries()
    MasterLibrary.load_all_packages()
    mocker.patch("src.util.user_input.input", return_value=randint(1, 100))
    mocker.patch("src.util.user_input.user_choose_from_list", side_effect=return_random)

    for _ in range(100):
        event = handler_new({})
        pprint(event)
        event = _run_random_command(event)
        process_command("", event)
    assert 0


def _run_random_command(event):
    random_commands = [
        "info",
        "bonus",
        "malus",
        "range",
        "equip",
        "attacker",
        "target",
        "overload",
        "cover",
        "charge",
        "aim",
        "auto",
        "move",
        "defend",
    ]
    command = choice(random_commands)
    try:
        event = process_command(command, event)
    except OutOfRangeError:
        pass
    return event
