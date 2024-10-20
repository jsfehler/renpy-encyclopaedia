"""renpy
init -85 python:
"""

class AddEntryError(Exception):
    """Raised when adding an entry to a parent fails."""
    pass


class GetEntryError(Exception):
    """Raised when getting an entry fails."""
