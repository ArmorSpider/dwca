from src.handler import build_attacker
from src.util.dict_util import pretty_print


def handler_rawdef(event):
    attacker = build_attacker(event)
    pretty_print(attacker.definition)
    return event
