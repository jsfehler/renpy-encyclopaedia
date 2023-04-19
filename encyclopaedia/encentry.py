from operator import itemgetter
from typing import Any, Optional, Union, TYPE_CHECKING

from renpy import store
from renpy.game import persistent

from .utils import enc_tint, string_to_list
from .eventemitter import EventEmitter

if TYPE_CHECKING:
    from .encyclopaedia import Encyclopaedia


class EncEntry(EventEmitter, store.object):
    """Stores an Entry's content.
    EncEntry instances should be added to an Encyclopaedia.

    Args:
        parent (Encyclopaedia, EncEntry)
        number (int) -
            The entry's number.
            If this is not set then it will be given a number automatically.
        name (str) -
            The name that will be displayed for the entry's button and labels.
        text (str, list) -
            The text that will be displayed when the entry is viewed.
        subject (str) -
            The subject to associate the entry with.
            Used for sorting and filtering.
        viewed (bool) -
            Determines if the entry has been seen or not.
            This should only be set if the Encyclopaedia is
            save-game independent.
        viewed_persistent(bool) -
            Determines if the Entry's viewed status uses persistent data.
        locked (bool) -
            Determines if the entry can be viewed or not. Defaults to False.
        locked_persistent(bool) -
            Determines if the Entry's locked status uses persistent data.
        image (str) -
            The image displayed with the Entry text. Default is None.
        locked_name (str) -
            Placeholder text for the name. Shown when the entry is locked.
        locked_text (str) -
            Placeholder text for the text. Shown when the entry is locked.
        locked_image (str) -
            Placeholder text for the image. Shown when the entry is locked.
        locked_image_tint (tuple) -
            If no specific locked image is provided,
            a tinted version of the image will be used.
            The amount of tinting can be set with RGB values in a tuple.

    Attributes:
        has_image (bool): True if an image was provided, else False.
        pages (int): Number of pages this entry contains.

        has_sub_entry (bool): If an entry has any sub-entries.
    """
    def __init__(self,
                 parent: Optional[Union['Encyclopaedia', 'EncEntry']] = None,
                 number: Optional[int] = None,
                 name: str = "",
                 text: Optional[str] = "",
                 subject: Optional[str] = "",
                 viewed: bool = False,
                 viewed_persistent: Optional[bool] = False,
                 locked: bool = False,
                 locked_persistent: Optional[bool] = False,
                 image: Optional[str] = None,
                 locked_name: Optional[str] = "???",
                 locked_text: Optional[str] = "???",
                 locked_image: Optional[str] = None,
                 locked_image_tint=(0.0, 0.0, 0.0)
                 ) -> None:

        self.tint_locked_image = False
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
            self.tint_locked_image = parent.tint_locked_image

        self.has_image = False
        if image is not None:
            self.has_image = True

            # If there's an image, but no locked image is specified,
            # tint the image and use it as the locked image.
            if locked_image is None and self.tint_locked_image:
                # Tuple is used to set the numbers that tint_locked_image()
                # uses to change the colour of a locked image
                self.locked_image = enc_tint(
                    self._image, locked_image_tint
                )

        self.pages = 1

        # The sub-entries and their position.
        # The parent EncEntry must be the first in the sub-entry list.
        self.sub_entry_list: list[list[Any]] = [[1, self]]

        self.has_sub_entry = False

        # Property: Set with Integer, get returns the page.
        self._current_page = 0

        self.callbacks: dict[str, list] = {
            "viewed": [],  # Run when this entry is viewed for the first time.
            "unlocked": [],  # Run when this entry is unlocked.
            "entry_unlocked": [],  # Run whenever a child entry is unlocked.
        }

        # When viewed is persistent, we get the viewed flag from persistent
        self.viewed_persistent = viewed_persistent
        if self.viewed_persistent:
            self._viewed = getattr(persistent, self._name + "_viewed")

    def __str__(self) -> str:
        return "EncEntry: {}".format(self.label)

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

        self._locked = new_value

        if self._locked is False:
            if isinstance(self.parent, EncEntry):
                self.parent.add_entry(self)
            else:
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
        """The number and name of the entry, in the format of 'number: name'
        """
        return "{:02}: {}".format(self.number, self.name)

    @property
    def current_page(self) -> 'EncEntry':
        """Get the sub-page that's currently viewing viewed.
            Setting this attribute should be done using an integer.
        """
        return self.sub_entry_list[self._current_page][1]

    @current_page.setter
    def current_page(self, val: int) -> None:
        self._current_page = val - 1

    def __get_entry_data(self, data: Any, locked_data: Any) -> Any:
        """Used by self.name, self.text, and self.image to control if
        the locked placeholder or actual entry data should be returned.

        Returns:
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

        Returns:
            bool: True if anything was added, else False
        """
        if entry.parent is not None and entry.parent != self:
            raise ValueError(
                "{} is already a sub-page of another EncEntry".format(entry),
            )

        # When a new entry has a number, ensure it's not already used.
        if entry.number is not None:
            if any(i for i in self.sub_entry_list if i[1].number == entry.number):
                raise ValueError(
                    "{} is already taken.".format(entry.number)
                )

        elif entry.number is None:
            entry.number = self.pages + 1

        entry.parent = self

        if [entry.number, entry] not in self.sub_entry_list:
            if entry.locked is False:
                self.sub_entry_list.append([entry.number, entry])
                self.sub_entry_list = sorted(
                    self.sub_entry_list,
                    key=itemgetter(0)
                )
                self.has_sub_entry = True

                self.pages = len(self.sub_entry_list)

                return True
        return False

    @property
    def word_count(self) -> int:
        """Get the word count for the EncEntry's text.

        Returns:
            int
        """
        count = 0
        for item in self._text:
            count += len(item.split())
        return count
