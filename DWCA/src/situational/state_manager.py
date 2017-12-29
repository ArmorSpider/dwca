from definitions import OVERLOADED, COVER


class StateManager(object):

    overloaded = False
    cover = 0

    @staticmethod
    def reset():
        StateManager.update({})

    @staticmethod
    def update(event):
        StateManager.overloaded = bool(event.get(OVERLOADED))
        StateManager.cover = int(event.get(COVER, 0))


def is_overloaded():
    return StateManager.overloaded


def get_cover():
    return StateManager.cover
