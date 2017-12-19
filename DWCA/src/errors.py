
class LibraryError(Exception):
    pass


class CLIError(Exception):
    pass


class NoMatchError(CLIError):
    pass


class WeaponNotFoundError(LibraryError):
    pass


class CharNotFoundError(LibraryError):
    pass


class NoFiremodeError(CLIError):
    pass


class ChooseFromListFailedError(CLIError):
    pass
