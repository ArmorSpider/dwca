from definitions import AIMED, OVERLOADED, CHARGE


class StateManager(object):

    aimed = False
    overloaded = False
    charge = False

    @staticmethod
    def update(event):
        StateManager.aimed = bool(event.get(AIMED))
        StateManager.overloaded = bool(event.get(OVERLOADED))
        StateManager.charge = bool(event.get(CHARGE))


def has_charged():
    return StateManager.charge


def is_aimed():
    return StateManager.aimed


def is_overloaded():
    return StateManager.overloaded
