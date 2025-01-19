from typing import TYPE_CHECKING

import renpy.exports as renpy
from renpy.store import DictEquality
from renpy.ui import Action

if TYPE_CHECKING:  # pragma: no cover
    from .book_ren import Book

"""renpy
init -84 python:
"""

class BookAction(Action, DictEquality):
    """Base Action that requires a Book as an argument.

    Should only be used for class inheritance.

    Args:
        book: The Book instance to use.
    """
    def __init__(self, book: 'Book') -> None:
        self.book = book


class BookPreviousPage(BookAction):
    """Change the current sub-entry being viewed.

    Used to switch from one page to another.
    """
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        result = self.book.previous_page()

        if result:
            renpy.restart_interaction()

    def get_sensitive(self) -> bool:
        """Determine if the button should be alive or not.

        Return:
            bool: True if the button should be alive, else False.
        """
        return not (self.book._unlocked_page_index - 1) < 0


class BookNextPage(BookAction):
    """Change the current sub-entry being viewed.

    Used to switch from one page to another.
    """
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        result = self.book.next_page()

        if result:
            renpy.restart_interaction()

    def get_sensitive(self) -> bool:
        """Determine if the button should be alive or not.

        Return:
            bool: True if the button should be alive, else False.
        """
        return not (self.book._unlocked_page_index + 1) >= len(self.book.unlocked_pages)
