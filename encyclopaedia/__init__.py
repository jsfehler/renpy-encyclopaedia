"""This file is used for documentation and testing.

Ren'Py has no use for it.
"""

from encyclopaedia.achentry_ren import AchievementEncEntry
from encyclopaedia.encentry_ren import EncEntry
from encyclopaedia.encentry_template_ren import EncEntryTemplate
from encyclopaedia.encyclopaedia_ren import Encyclopaedia
from encyclopaedia.text_block_ren import text_block
from encyclopaedia.version import __version__  # noqa: F401

__all__ = [
    'AchievementEncEntry',
    'Encyclopaedia',
    'EncEntry',
    'EncEntryTemplate',
    'text_block',
]
