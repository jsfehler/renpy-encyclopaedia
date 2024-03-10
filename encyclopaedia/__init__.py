"""This file is used for documentation and testing.

Ren'Py has no use for it.
"""

from encyclopaedia.encentry_ren import EncEntry
from encyclopaedia.encyclopaedia_ren import Encyclopaedia
from encyclopaedia.encentry_template_ren import EncEntryTemplate
from encyclopaedia.text_block_ren import text_block
from encyclopaedia.version import __version__  # noqa: F401


__all__ = [
    'Encyclopaedia',
    'EncEntry',
    'EncEntryTemplate',
    'text_block'
]
