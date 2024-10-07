"""renpy
init -85 python:
"""

class AddEntryError(Exception):
    """Raised when adding an EncEntry to a parent fails."""
    pass
