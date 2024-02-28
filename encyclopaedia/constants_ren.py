"""renpy
init -85 python:
"""  # NOQA D205
from enum import Enum


class Direction(Enum):
    """Constants for the direction when scrolling through EncEntry."""
    BACKWARD = -1
    FORWARD = 1


class SortMode(Enum):
    """Constants for different ways of sorting an Encyclopaedia."""
    NUMBER = 0
    ALPHABETICAL = 1
    REVERSE_ALPHABETICAL = 2
    SUBJECT = 3
    UNREAD = 4
