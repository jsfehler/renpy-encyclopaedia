from functools import partial

from .encentry import EncEntry


def EncEntryTemplate(**kwargs):
    return partial(EncEntry, **kwargs)
