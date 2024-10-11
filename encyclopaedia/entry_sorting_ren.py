from .types_ren import ENTRY_TYPE

"""renpy
init python:
"""
from operator import attrgetter  # NOQA E402


def push_locked_to_bottom(seq: list[ENTRY_TYPE]) -> list[ENTRY_TYPE]:
    """Move all the locked entries in a list of entries to the bottom of the list.

    Args:
        seq: The sequence of EncEntry to sort.

    Return:
        Sorted version of the given sequence
    """
    new_list = sorted(seq, reverse=True, key=attrgetter('locked'))

    del seq[:]

    for item in new_list:
        seq.append(item)

    return seq
