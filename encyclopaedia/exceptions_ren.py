"""renpy
init -85 python:
"""

class AddEntryError(Exception):
    """Raised when adding an entry to a parent fails."""
    pass


class GetEntryError(Exception):
    """Raised when getting an entry fails."""
    pass


class UnknownEntryError(Exception):
    """Raised when looking for an entry that is not in an Encyclopaedia."""
    pass
