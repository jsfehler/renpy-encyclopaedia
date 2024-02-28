from .encentry_ren import EncEntry

"""renpy
init python:
"""

from functools import partial  # NOQA E402


def EncEntryTemplate(**kwargs) -> partial[EncEntry]:  # NOQA N802
    """A template generator for EncEntry.

    Any valid argument for EncEntry can be used in EncEntryTemplate.

    Example:
        >>> Fruit = EncEntryTemplate(subject='Fruit', locked=True)
        >>> apple = Fruit(name='Apple')
    """
    return partial(EncEntry, **kwargs)
