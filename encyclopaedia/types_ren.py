from typing import Union

from .encentry_ren import EncEntry
from .book import Book

"""renpy
init -85 python:
"""

ENTRY_TYPE = Union[Book, EncEntry]
