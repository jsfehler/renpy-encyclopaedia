from typing import TYPE_CHECKING

from renpy import store

if TYPE_CHECKING:
    from .encyclopaedia_ren import Encyclopaedia
    from .encentry_ren import EncEntry

"""renpy
init python:
"""


def set_encentry_from_text_anchor(value: str) -> None:
    """Parse a Ren'Py text anchor to open an EncEntry.

    This function is added to Ren'Py's config.hyperlink_handlers with the key
    "set_entry"

    Args:
        value: A string in the format of "Encyclopaedia->EncEntry"
    """
    enc_name, entry_name = value.split('->')

    enc: 'Encyclopaedia' = getattr(store, enc_name)
    entry: 'EncEntry' = getattr(store, entry_name)

    enc.SetEntry(entry)()
