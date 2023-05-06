from operator import attrgetter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .encentry import EncEntry


def push_locked_to_bottom(seq: list['EncEntry']) -> list['EncEntry']:
    """Move all the locked entries in a list of entries to
    the bottom of the list.

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
