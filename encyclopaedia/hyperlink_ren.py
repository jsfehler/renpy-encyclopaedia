from typing import TYPE_CHECKING

from renpy import store
from renpy.store import ShowMenu

from .book import Book
from .exceptions_ren import InvalidEntryAnchorError
from .types_ren import ENTRY_TYPE

if TYPE_CHECKING:  # pragma: no cover
    from .encyclopaedia_ren import Encyclopaedia

"""renpy
init -85 python:
"""


def set_encentry_from_text_anchor(value: str) -> None:
    """Parse a Ren'Py text anchor to open an EncEntry.

    This function is added to Ren'Py's config.hyperlink_handlers with the key
    "set_entry"

    Args:
        value: A string in the format of "(encyclopaedia)->(entry)->(page number)"
    """
    pieces = value.split('->')

    if len(pieces) <= 1:
        raise InvalidEntryAnchorError(f"Missing Arguments: {value}")

    try:
        enc_name, entry_name, page_num = pieces
    except ValueError:
        enc_name, entry_name = pieces
        page_num = 0

    enc: 'Encyclopaedia' = getattr(store, enc_name)
    entry: ENTRY_TYPE = getattr(store, entry_name)

    if isinstance(entry, Book):
        entry.set_active_page(int(page_num))

    enc.active = entry

    # Open the Encyclopaedia, the screen will open the active entry for us.
    ShowMenu(enc.hyperlink_screen, enc=enc)()
