from definitions import AIMED, OVERLOADED, CHARGE, COVER


class StateManager(object):

    aimed = False
    overloaded = False
    charge = False
    cover = 0

    @staticmethod
    def reset():
        StateManager.update({})

    @staticmethod
    def update(event):
        StateManager.aimed = bool(event.get(AIMED))
        StateManager.overloaded = bool(event.get(OVERLOADED))
        StateManager.charge = bool(event.get(CHARGE))
        StateManager.cover = int(event.get(COVER, 0))


def has_charged():
    return StateManager.charge


def is_aimed():
    return StateManager.aimed


def is_overloaded():
    return StateManager.overloaded


def get_cover():
    return StateManager.cover
