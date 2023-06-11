from typing import TYPE_CHECKING

from renpy import store
from renpy.color import Color
from renpy.display.transform import Transform
from renpy.game import persistent
from renpy.store import TintMatrix

from .utils_ren import string_to_list
from .eventemitter_ren import EventEmitter
from .constants_ren import Direction

if TYPE_CHECKING:  # pragma: no cover
    from .encyclopaedia_ren import Encyclopaedia


"""renpy
init python:
"""

from operator import attrgetter  # NOQA E402
from typing import Any, Callable, Optional, Union  # NOQA E402


class EncEntry(EventEmitter, store.object):
    """Store an Entry's content.

    EncEntry instances should be added to an Encyclopaedia or another EncEntry.

    Args:
        parent: The parent container for the EncEntry.
        number: The entry's number.
            If this is not set then it will be given a number automatically.
        name: Title, normally used for buttons and headings.
        text: The text that will be displayed when the entry is viewed.
        subject: The subject to associate the entry with.
            Used for sorting and filtering.
        viewed: Set the viewed status of the EncEntry. Default is False.
            Only use if the Encyclopaedia is save-game independent.
        viewed_persistent: Use persistent data for recording viewed status.
        locked: Set the locked status of the EncEntry. Default is False.
        locked_persistent: Use persistent data for recording locked status.
        image: The image displayed with the Entry text. Default is None.
        locked_name: Placeholder text for the name. Shown when the entry is locked.
        locked_text: Placeholder text for the text. Shown when the entry is locked.
        locked_image: Placeholder image for the image. Shown when the entry is locked.
        locked_image_tint: If no specific locked image is provided,
            a tinted version of the image will be used.
            The amount of tinting can be set with RGB values in a tuple.

    Attributes:
        has_image: True if an image was provided, else False.
        pages: List of all the pages this entry contains.
        has_pages: If an entry has any sub-entries.
    """
    def __init__(self,
                 parent: Optional[Union['Encyclopaedia', 'EncEntry']] = None,
                 number: Optional[int] = None,
                 name: str = "",
                 text: Union[str, list[str]] = "",
                 subject: str = "",
                 viewed: bool = False,
                 viewed_persistent: Optional[bool] = False,
                 locked: bool = False,
                 locked_persistent: Optional[bool] = False,
                 image: Optional[str] = None,
                 locked_name: str = "???",
                 locked_text: str = "???",
                 locked_image: Optional[str] = None,
                 locked_image_tint: tuple[float, float, float] = (0.0, 0.0, 0.0)
                 ) -> None:

        # Place the entry into the assigned Encyclopaedia or EncEntry.

        # self.parent is set to None so that add_entry doesn't think
        # this EncEntry is already inside an Encyclopaedia.
        self.parent: Optional[Union['Encyclopaedia', 'EncEntry']] = None
        self.number = number

        self.locked_name = locked_name
        self.locked_text = string_to_list(locked_text)
        self.locked_image = locked_image

        self._name = name
        self._text = string_to_list(text)
        self._viewed = viewed
        self.subject = subject
        self._locked = locked
        self._image = image

        self.locked_persistent = locked_persistent
        if self.locked_persistent:
            self._locked = getattr(persistent, self._name + "_locked")

        if parent is not None:
            parent.add_entry(self)

        self.has_image: bool = False
        if image is not None:
            self.has_image = True

            # If there's an image, but no locked image is specified,
            # tint the image and use it as the locked image.
            if locked_image is None:
                c = Color(rgb=locked_image_tint)
                self.locked_image = Transform(image, matrixcolor=TintMatrix(c))

        # Setup pages

        # The current instance must be the first in the sub-entry list.
        self.pages: list['EncEntry'] = [self]

        # Cache unlocked pages
        self.unlocked_pages: list['EncEntry'] = [self]

        self.has_pages = False

        # Relative to the unlocked pages, cache the position of the active page.
        self._unlocked_page_index = 0

        self.callbacks: dict[str, list[Callable[['EncEntry'], None]]] = {
            "viewed": [],  # Run when this entry is viewed for the first time.
            "unlocked": [],  # Run when this entry is unlocked.
            "entry_unlocked": [],  # Run whenever a child entry is unlocked.
        }

        # When viewed is persistent, we get the viewed flag from persistent
        self.viewed_persistent = viewed_persistent
        if self.viewed_persistent:
            self._viewed = getattr(persistent, self._name + "_viewed")

    def __repr__(self) -> str:
        return f"EncEntry(number={self.number}, name={self.name})"

    def __str__(self) -> str:
        return self.label

    @property
    def locked(self) -> bool:
        """Determine if the entry's data can be viewed or not.
            Changing this variable will modify the entry's locked status.
        """
        return self._locked

    @locked.setter
    def locked(self, new_value: bool) -> None:
        if self.locked_persistent:
            setattr(persistent, self._name + "_locked", new_value)

        # Only run if the entry was locked
        if (self._locked is not False) and (new_value is False):
            self._locked = new_value

            if self.parent is not None:
                self.parent.add_entry_to_unlocked_entries(self)
                self.parent.emit("entry_unlocked")

            self.emit("unlocked")

    @property
    def viewed(self) -> bool:
        """Determines if the entry has been viewed or not.
            Changing this variable will modify the entry's viewed status.
        """
        return self._viewed

    @viewed.setter
    def viewed(self, new_value: bool) -> None:
        if self.viewed_persistent:
            setattr(persistent, self._name + "_viewed", new_value)

        self._viewed = new_value

    @property
    def label(self) -> str:
        """The number and name of the entry, in the format of 'number: name'.
        """
        number = str(self.number).zfill(2)

        return f"{number}: {self.name}"

    @property
    def current_page(self) -> 'EncEntry':
        """Get the sub-page that's currently viewing viewed.

        Setting this attribute should be done using an integer.
        """
        return self.unlocked_pages[self._unlocked_page_index]

    def __get_entry_data(self, data: Any, locked_data: Any) -> Any:
        """Used by self.name, self.text, and self.image to control if
        the locked placeholder or actual entry data should be returned.

        Return:
            If True or None, return the data requested,
            otherwise the placeholder for the data
        """
        if self.locked or self.locked is None:
            return locked_data
        return data

    @property
    def name(self) -> str:
        """The name for the entry. Return placeholder when entry is locked."""
        return self.__get_entry_data(self._name, self.locked_name)

    @name.setter
    def name(self, val: str) -> None:
        self._name = val

        self.viewed = False

    @property
    def text(self) -> list[str]:
        """The text for the entry. Return placeholder when entry is locked."""
        return self.__get_entry_data(self._text, self.locked_text)

    @text.setter
    def text(self, val: list[str]) -> None:
        self._text = val

        self.viewed = False

    @property
    def image(self) -> str:
        """The image for the entry. Return placeholder when entry is locked."""
        return self.__get_entry_data(self._image, self.locked_image)

    @image.setter
    def image(self, val: str) -> None:
        self.has_image = True
        self._image = val

        self.viewed = False

    def add_entry(self, entry: 'EncEntry') -> bool:
        """Add multiple pages to the entry in the form of sub-entries.

        Args:
            entry: The entry to add as a sub-entry.

        Return:
            True if anything was added, else False.

        Raise:
            AttributeError: If the entry is already the page of another entry.
            ValueError: If the entry has a number that is already taken.
        """
        if entry.parent is not None and entry.parent != self:
            raise AttributeError(
                f"{entry} is already a page of {self.parent}",
            )

        # When a new entry has a number, ensure it's not already used.
        if entry.number is not None:
            if any(i for i in self.pages if i.number == entry.number):
                raise ValueError(
                    f"{entry.number} is already taken."
                )

        elif entry.number is None:
            entry.number = len(self.pages) + 1

        entry.parent = self

        if entry not in self.pages:
            if entry.locked is False:
                self.add_entry_to_unlocked_entries(entry)

            self.pages.append(entry)
            # Sort by number.
            self.pages = sorted(
                self.pages,
                key=attrgetter('number'),
            )
            self.has_pages = True

            return True

        return False

    def add_entry_to_unlocked_entries(self, entry: 'EncEntry') -> None:
        """Add an entry to the list of unlocked entries.

        Args:
            entry: The Entry to add to the unlocked entries list.
        """

        self.unlocked_pages.append(entry)

        # Remove duplicates
        self.unlocked_pages = list(set(self.unlocked_pages))

        self.unlocked_pages = sorted(
            self.unlocked_pages,
            key=attrgetter('number'),
        )

    def _change_page(self, direction: Direction) -> bool:
        """Change the current sub-entry page."""

        new_page_number = self._unlocked_page_index + direction.value

        # Don't allow moving beyond bounds.
        if new_page_number < 0:
            return False

        elif new_page_number > len(self.pages):
            return False

        self._unlocked_page_index = new_page_number

        # Update viewed state
        if self.current_page.viewed is False:
            self.current_page.viewed = True

        return True

    def previous_page(self) -> bool:
        """Set the previous sub-entry page as the current page."""
        return self._change_page(Direction.BACKWARD)

    def next_page(self) -> bool:
        """Set the next sub-entry page as the current page."""
        return self._change_page(Direction.FORWARD)

    @property
    def word_count(self) -> int:
        """Get the word count for the EncEntry's text.

        Return:
            The number of words in the EncEntry.
        """
        count = 0
        for item in self._text:
            count += len(item.split())
        return count
