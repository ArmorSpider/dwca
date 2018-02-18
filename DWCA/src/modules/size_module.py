from src.handler import build_target
from src.modifiers.roll_modifier import add_roll_mod, SIZE_MOD


def handler_size(event):
    target = build_target(event)
    event = add_roll_mod(event, target.size_bonus, SIZE_MOD)
    return event
