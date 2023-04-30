from enum import Enum


class SortMode(Enum):
    """Constants for different ways of sorting an Encyclopaedia."""
    NUMBER = 0
    ALPHABETICAL = 1
    REVERSE_ALPHABETICAL = 2
    SUBJECT = 3
    UNREAD = 4
