from .encentry_ren import EncEntry
"""renpy
init python:
"""
from functools import partial  # NOQA E402


def EncEntryTemplate(**kwargs) -> partial[EncEntry]:
    return partial(EncEntry, **kwargs)
