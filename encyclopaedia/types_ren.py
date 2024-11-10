from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .book import Book
    from .encentry_ren import EncEntry

"""renpy
init -85 python:
"""
from typing import Union  # NOQA E402

ENTRY_TYPE = Union['Book', 'EncEntry']
