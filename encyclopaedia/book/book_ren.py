from typing import TYPE_CHECKING

from renpy import store
from renpy.game import persistent

from .actions_ren import (
    BookNextPage,
    BookPreviousPage,
)
from ..constants_ren import Direction
from ..eventemitter_ren import EventEmitter
from ..exceptions_ren import AddEntryError

if TYPE_CHECKING:  # pragma: no cover
    from ..encyclopaedia_ren import Encyclopaedia
    from ..encentry_ren import EncEntry

"""renpy
init -84 python:
"""
from math import floor  # NOQA E402
from operator import attrgetter  # NOQA E402
from typing import Any, Callable, Optional, Union  # NOQA E402


class Book(EventEmitter, store.object):
    """Container for EncEntry which have a strong relationship with each other.

    A Book should be placed inside an Encyclopaedia.
    When sorted and/or filtered, the Book's attributes will be used.
    """
    def __init__(
        self,
        number: Optional[int] = None,
        parent: Optional['Encyclopaedia'] = None,
        title: str = "",
        subject: str = "",
        locked: bool = False,
        locked_persistent: Optional[bool] = False,
        locked_title: str = "???",
    ) -> None:
        self.parent: Optional['Encyclopaedia'] = None
        self.number = number
        self.subject = subject
        self.locked_title = locked_title

        self._title = title
        self._locked = locked

        # When locked status is persistent, get the value from renpy.persistent.
        self.locked_persistent = locked_persistent
        if self.locked_persistent:
            persistent_key = self._get_persistent_name()

            self._locked = getattr(persistent, persistent_key)
            # persistent variables default to None when not found.
            if self._locked is None:
                self._locked = locked
                setattr(persistent, persistent_key, locked)

        if parent is not None:
            parent.add_entry(self)

        self.pages: list['EncEntry'] = []
        self.unlocked_pages: list['EncEntry'] = []

        # Cache the current list index of the active page.
        self._unlocked_page_index: int = 0

        self.actions = PageActions(self)

        self.callbacks: dict[str, list[Callable[['EventEmitter'], None]]] = {
            "unlocked": [],  # Run when this Book is unlocked.
            "entry_unlocked": [],  # Run whenever a page is unlocked.
        }

        self._word_count = 0

    def _get_persistent_name(self) -> str:
        """Get a persistent key for the Book's persistent data."""
        normalized_title = self._title.lower().replace(' ', '_')
        rv = f"{normalized_title}_locked"
        return rv

    def __repr__(self) -> str:  # NOQA D105
        return f"Book(number={self.number}, title={self.title})"

    def __str__(self) -> str:  # NOQA D105
        return f"{self.title}"

    def __get_entry_data(self, data: Any, locked_data: Any) -> Any:
        """Used by (name, text, image) attributes to check if the placeholder should be returned.

        Return:
            If True or None, return the data requested,
            otherwise the placeholder for the data
        """
        if self.locked or self.locked is None:
            return locked_data
        return data

    @property
    def title(self) -> str:
        """The title of the Book."""
        return self.__get_entry_data(self._title, self.locked_title)

    @property
    def name(self) -> str:
        """Alias for title, used for sorting in an Encyclopaedia."""
        return self.__get_entry_data(self._title, self.locked_title)

    @property
    def locked(self) -> bool:
        """The locked status of the Book."""
        return self._locked

    @locked.setter
    def locked(self, new_value: bool) -> None:
        if self.locked_persistent:
            persistent_key = self._get_persistent_name()
            setattr(persistent, persistent_key, new_value)

        # Only run if the Book was locked.
        if (self._locked) and (new_value is False):
            if self.parent is not None:
                self.parent.add_entry_to_unlocked_entries(self)
                self.parent.emit("entry_unlocked")

            self.emit("unlocked")

        self._locked = new_value

    @property
    def viewed(self) -> bool:
        """Determine if the Book has been viewed or not.

        Return:
            False if any page in the Book has not been viewed, else True.
        """
        for page in self.pages:
            if not page.viewed:
                return False
        return True

    @property
    def active(self) -> 'EncEntry':
        """Get the page that's currently being viewed."""
        return self.pages[self._unlocked_page_index]

    @property
    def current_page(self) -> 'EncEntry':
        """Alias for active. Used by screens."""
        return self.active

    @property
    def percentage_unlocked(self) -> float:
        """Get the percentage of the Book that's unlocked.

        Return:
            Number between 0.0 and 1.0

        Raises:
            ZeroDivisionError: If the Book is empty
        """
        float_size = len(self.unlocked_pages)
        float_size_all = len(self.pages)

        try:
            amount_unlocked = float_size / float_size_all
        except ZeroDivisionError as err:
            raise ZeroDivisionError(
                'Cannot calculate percentage unlocked of empty Book',
            ) from err

        return amount_unlocked

    @property
    def word_count(self) -> int:
        """Get the word count for the entire Book.

        All the text from all the pages in the book will be counted.

        Return:
            The number of words in the Book.
        """
        return self._word_count

    def _recalculate_word_count(self) -> int:
        """Recalculate the word count of the book.

        This is used so we don't have to recalculate the word count
        every time it's checked. We only run this when an entry is added.

        Returns:
            The new word count
        """
        count = 0
        for page in self.pages:
            count += page.word_count

        self._word_count = count
        return count

    def add_entry(self, entry: 'EncEntry') -> bool:
        """Add an EncEntry to this Book.

        Returns:
            True if the operation was a success

        Raises:
            AddEntryError
        """
        if entry.parent is not None and entry.parent != self:
            raise AddEntryError(
                f"<{entry}> is already a page of {self.parent}",
            )

        if entry.number is None:
            raise AddEntryError(f"<{entry} does not have a number.")

        if any(i for i in self.pages if i.number == entry.number):
            raise AddEntryError(
                f"{entry.number} is already taken.",
            )

        if entry.subject:
            raise AddEntryError(
                "Entries inside a Book cannot have their own subject.",
            )

        entry.parent = self
        entry.subject = self.subject
        entry.page_number = entry.number + 1

        self.pages.append(entry)
        self.pages = sorted(
            self.pages,
            key=attrgetter('number'),
        )

        if entry.locked is False:
            self.add_entry_to_unlocked_entries(entry)

        self._recalculate_word_count()

        return True

    def add_entry_to_unlocked_entries(self, entry: 'EncEntry') -> None:
        """Add an entry to the list of unlocked entries.

        Args:
            entry: The Entry to add to the unlocked entries list.
        """
        self.unlocked_pages.append(entry)

        self.unlocked_pages = sorted(
            self.unlocked_pages,
            key=attrgetter('number'),
        )

    def set_active_page(self, page_number: int) -> None:
        """Set a page to be active, based on the page number.

        Arguments:
            page_number: The number of the page to set.
        """
        if page_number < 0:
            raise ValueError("Invalid page number.")

        if page_number > len(self.pages):
            raise ValueError("Invalid page number.")

        self._unlocked_page_index = page_number

    def _change_page(self, direction: Direction) -> bool:
        """Change the current active page."""
        new_page_number = self._unlocked_page_index + direction.value

        # Don't allow moving beyond bounds.
        if new_page_number < 0:
            return False

        elif new_page_number >= len(self.pages):
            return False

        self._unlocked_page_index = new_page_number

        # Update viewed state
        if self.active.viewed is False:
            self.active.viewed = True

        return True

    def previous_page(self) -> bool:
        """Set the previous page as the current page."""
        return self._change_page(Direction.BACKWARD)

    def next_page(self) -> bool:
        """Set the next page as the current page."""
        return self._change_page(Direction.FORWARD)


class PageActions:
    """Actions used to navigate a Book."""
    def __init__(self, parent: 'Book') -> None:
        self.parent = parent

    def PreviousPage(self) -> BookPreviousPage:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return BookPreviousPage(book=self.parent)

    def NextPage(self) -> BookNextPage:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return BookNextPage(book=self.parent)
