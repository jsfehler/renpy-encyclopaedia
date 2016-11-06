from operator import attrgetter


def push_locked_to_bottom(seq):
    """Moves all the locked entries in a list of entries to
    the bottom of the list.

    Args:
        seq: The sequence of EncEntry to sort.

    Returns:
        list: Sorted version of the given sequence
    """
    new_list = sorted(seq, reverse=True, key=attrgetter('locked'))

    del seq[:]

    for item in new_list:
        seq.append(item)

    return seq
