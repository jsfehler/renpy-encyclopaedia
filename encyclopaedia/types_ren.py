from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .encentry_ren import EncEntry
    from .book import Book

"""renpy
init -85 python:
"""
from typing import Union  # NOQA E402


ENTRY_TYPE = Union['Book', 'EncEntry']
