
class LibraryError(Exception):
    pass


class WeaponNotFoundError(LibraryError):
    pass


class CharNotFoundError(LibraryError):
    pass
