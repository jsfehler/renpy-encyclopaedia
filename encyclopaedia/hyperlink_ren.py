from typing import TYPE_CHECKING

from renpy import store
from renpy.store import ShowMenu

if TYPE_CHECKING:  # pragma: no cover
    from .encyclopaedia_ren import Encyclopaedia
    from .encentry_ren import EncEntry

"""renpy
init -85 python:
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

    enc.active = entry

    # Open the Encyclopaedia, the screen will open the active entry for us.
    ShowMenu('encyclopaedia_list', enc=enc)()
