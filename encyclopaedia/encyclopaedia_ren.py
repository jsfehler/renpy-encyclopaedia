from typing import TYPE_CHECKING

from renpy import store

from .actions_ren import (
    ClearFilter,
    CloseActiveEntry,
    FilterBySubject,
    NextEntry,
    NextPage,
    PreviousEntry,
    PreviousPage,
    ResetSubPage,
    SetEntry,
    SortEncyclopaedia,
    ToggleShowLockedButtonsAction,
    ToggleShowLockedEntryAction,
)
from .book import Book
from .constants_ren import Direction, SortMode
from .entry_sorting_ren import push_locked_to_bottom
from .eventemitter_ren import EventEmitter
from .exceptions_ren import AddEntryError, UnknownEntryError
from .types_ren import ENTRY_TYPE

if TYPE_CHECKING:  # pragma: no cover
    from .encentry_ren import EncEntry

"""renpy
init python:
"""
from math import floor  # NOQA E402
from operator import attrgetter  # NOQA E402
from typing import Callable, Optional, Union, cast  # NOQA E402


class Encyclopaedia(EventEmitter, store.object):
    """Container to manage the behaviour of a collection of EncEntry objects.

    Args:
        sorting_mode: How entries are sorted. Default is SortMode.NUMBER.
        show_locked_buttons: If True, locked entries show a
            placeholder label on the listing screen.
        show_locked_entry: If True, locked entries can be viewed, but
            the data is hidden from view with a placeholder.
        list_screen: The Ren'Py screen to display the list of entries.
        entry_screen: The Ren'Py screen to display an open entry.
        hyperlink_screen: The Ren'Py screen to display an entry opened from a
            hyperlink.
        name: A optional name for the Encyclopaedia.

    Attributes:
        all_entries: All entries, regardless of status.
        unlocked_entries: Only unlocked entries.
        filtered_entries: Entries that match a subject filter.
        filtering: The subject name being used as a filter.
        size_all: Length of self.all_entries.
        size_unlocked: Length of self.unlocked_entries.
        reverse_sorting: Should sorting occur in reverse or not.
        nest_alphabetical_sort: Should alphabetical sorting display
            each letter as a subject.
        current_position: Index for the current entry open.
        subjects: Collection of every subject.
        active: The currently open entry.
        locked_at_bottom: True if locked entries should appear at
            the bottom of the entry list or not.
    """

    def __init__(self,
                 sorting_mode: SortMode = SortMode.NUMBER,
                 show_locked_buttons: bool = False,
                 show_locked_entry: bool = False,
                 list_screen: str = 'encyclopaedia_list',
                 entry_screen: str = 'encyclopaedia_entry',
                 hyperlink_screen: str = 'encyclopaedia_list',
                 name: str = '',
                 ) -> None:
        self._sorting_mode = sorting_mode
        self._reverse_sorting: bool = False

        self.show_locked_buttons = show_locked_buttons
        self.show_locked_entry = show_locked_entry
        self.list_screen = list_screen
        self.entry_screen = entry_screen
        self.hyperlink_screen = hyperlink_screen
        self.name = name

        self.all_entries: list[ENTRY_TYPE] = []
        self.unlocked_entries: list[ENTRY_TYPE] = []
        self.filtered_entries: list[ENTRY_TYPE] = []

        self.filtering: Union[bool, str] = False

        self.nest_alphabetical_sort: bool = True

        self.current_position: int = 0

        self.subjects: list[str] = []

        self.active: Optional[ENTRY_TYPE] = None
        self._current_entries = self.all_entries

        self.locked_at_bottom: bool = True

        self.callbacks: dict[str, list[Callable[['EventEmitter'], None]]] = {
            "entry_unlocked": [],  # Run whenever a child entry is unlocked.
        }

    def __repr__(self) -> str:  # NOQA D105
        return f"Encyclopaedia(name={self.name}, length={len(self.all_entries)})"

    def __str__(self) -> str:  # NOQA D105
        return f"Encyclopaedia: {self.name}"

    def __len__(self) -> int:
        """The total number of entries, relative to if locked ones are shown or not."""
        rv = len(self.viewable_entries)
        return rv

    @property
    def viewable_entries(self) -> list[ENTRY_TYPE]:
        """Get the list of entries which are currently viewable."""
        if self.show_locked_entry:
            return self.all_entries
        else:
            return self.unlocked_entries

    @property
    def current_entries(self) -> list[ENTRY_TYPE]:
        """Get all the entries which should be visible to the user.

        Return:
            List of EncEntries. If filtering, only entries that match the
            filter are returned.
        """
        rv = self.unlocked_entries

        if self.filtering:
            rv = self.filtered_entries
        elif self.show_locked_buttons:
            rv = self.all_entries

        return rv

    @property
    def current_entry(self) -> ENTRY_TYPE:
        """Get the entry at current_position.

        If show locked entries, pull from all_entries.
        Else, pull from unlocked_entries.

        Return:
            EncEntry
        """
        entry = self.viewable_entries[self.current_position]
        return entry

    @property
    def percentage_unlocked(self) -> float:
        """Get the percentage of the Encyclopaedia that's unlocked.

        Return:
            Number between 0.0 and 1.0

        Raises:
            ZeroDivisionError: If the Encyclopaedia is empty
        """
        float_size = len(self.unlocked_entries)
        float_size_all = len(self.all_entries)

        try:
            amount_unlocked = float_size / float_size_all
        except ZeroDivisionError as err:
            raise ZeroDivisionError(
                'Cannot calculate percentage unlocked of empty Encyclopaedia',
            ) from err

        percentage = floor(amount_unlocked * 100)
        return percentage

    @property
    def sorting_mode(self) -> SortMode:
        """Get the current sorting mode of the Encyclopaedia."""
        return self._sorting_mode

    @property
    def reverse_sorting(self) -> bool:
        """Get the direction of the current sorting.

        Returns:
            True if sorting is reversed, else False.
        """
        return self._reverse_sorting

    def _sort_entries(self, entries: list[ENTRY_TYPE]) -> None:
        """Sort an entry list.

        The Encyclopaedia's `sorting_mode` and `reverse_sorting` attributes
        are used for sorting.

        Args:
            entries: The EncEntry list to sort.
        """
        sorting_mode = self.sorting_mode
        reverse = self.reverse_sorting

        # The reverse of SortMode.ALPHABETICAL is the equivalent of
        # SortMode.REVERSE_ALPHABETICAL and vice versa.
        reverse_alphabetical = False
        if (sorting_mode == SortMode.REVERSE_ALPHABETICAL) and not reverse:
            reverse_alphabetical = True

        elif (sorting_mode == SortMode.ALPHABETICAL) and reverse:
            reverse_alphabetical = True

        if sorting_mode == SortMode.NUMBER:
            entries.sort(key=attrgetter('number'))
        else:
            # If not number, always sort by name first.
            entries.sort(reverse=reverse_alphabetical, key=attrgetter('name'))

            if sorting_mode == SortMode.UNREAD:
                entries.sort(reverse=reverse, key=attrgetter('viewed'))

            elif sorting_mode == SortMode.SUBJECT:
                entries.sort(reverse=reverse, key=attrgetter('subject'))

            if self.locked_at_bottom:
                push_locked_to_bottom(entries)

    def _add_entry_to_unlocked_entries(self, entry: ENTRY_TYPE) -> None:
        """Add an entry to the list of unlocked entries.

        Args:
            entry: The Entry to add to the unlocked entries list.
        """
        self.unlocked_entries.append(entry)

        # Remove duplicates
        self.unlocked_entries = list(set(self.unlocked_entries))

        self._sort_entries(entries=self.unlocked_entries)

    def _find_closest_free_number(self) -> int:
        """Find the closest unused EncEntry number."""
        if len(self.all_entries) > 0:
            # Get all possible numbers
            last_number = cast(int, self.all_entries[-1].number)

            all_numbers = range(last_number + 1)[1:]
            used_numbers = [item.number for item in self.all_entries]
            free_numbers = set(all_numbers) - set(used_numbers)

            # If there are unused numbers.
            if len(free_numbers) > 0:
                return min(free_numbers)
            # Else add a new number.
            else:
                return len(self.all_entries) + 1

        # Catch the first EncEntry to be entered.
        else:
            return 1

    def add_entry(self, entry: ENTRY_TYPE) -> None:
        """Add an entry to the Encyclopaedia's internal lists and sorts it.

        Attempts to create duplicates are softly ignored.
        subjects list is updated when a new entry is added.

        Args:
            entry: The Entry to add to the Encyclopaedia
        """
        if entry.parent is not None and entry.parent != self:
            raise AddEntryError(
                f"<{entry}> already has a parent: <{entry.parent}>",
            )

        # When a new entry has a number, ensure it's not already used.
        if entry.number is not None:
            if any(i for i in self.all_entries if i.number == entry.number):
                raise AddEntryError(f"{entry.number} is already taken.")

        elif entry.number is None:
            entry.number = self._find_closest_free_number()

        self.all_entries.append(entry)
        entry.parent = self

        # Ensure no duplicates in the entry lists.
        self.all_entries = list(set(self.all_entries))

        # Ensure correct sorting of entry lists.
        self._sort_entries(entries=self.all_entries)

        if entry.locked is False:
            self._add_entry_to_unlocked_entries(entry)

        self.subjects.append(entry.subject)
        self.subjects = list(set(self.subjects))
        self.subjects.sort()

    def sort(self, mode: Union[SortMode, None] = None, reverse: bool = False) -> None:
        """Sort the entries in the Encyclopaedia.

        The attribute `sorting_mode` will be set to the value of `mode`.

        Args:
            mode: The sorting mode to use.
                  If None, the attribute `sorting_mode` will be used.
            reverse: If the sorting should be done in reverse or not.
        """
        if mode:
            self._sorting_mode = mode

        self._reverse_sorting = reverse

        self._sort_entries(entries=self.current_entries)

    @property
    def word_count(self) -> int:
        """Get the total word count for the Encyclopaedia.

        Return:
            The number of words in every EncEntry in the Encyclopaedia.
        """
        count = 0
        for entry in self.all_entries:
            count += entry.word_count
        return count

    def _build_subject_filter(self, subject: str) -> None:
        """Build an encyclopaedia's filtered_entries based on subject.

        Args:
            subject: The subject for the filter.
        """
        if self.show_locked_buttons is False:
            entries = self.unlocked_entries
        else:
            entries = self.all_entries

        self.filtered_entries = [i for i in entries if i.subject == subject]

    def _change_active_entry_viewed_status(self) -> bool:
        """Change the viewed status of the active Entry.

        Return:
            True if status was changed, else False
        """
        if self.active is None:
            raise ValueError(
                'Tried to change active entry viewed status with no active entry.',
            )
        if self.active.locked is False:
            entry = None

            if isinstance(self.active, Book):
                # When Book, set the first page to viewed, not the Book.
                entry = self.active.active
            else:
                entry = self.active

            # Mark the entry as viewed.
            entry.viewed = True

            return True

        return False

    def set_entry(self, entry: ENTRY_TYPE) -> None:
        """Set an Entry as active.

        Args:
            entry: The Entry to set.

        Raises:
            ValueError: If the entry cannot be set.
        """
        try:
            target_position = self.viewable_entries.index(entry)
        except ValueError as e:
            if entry not in self.all_entries:
                raise UnknownEntryError(f"{entry} is not in this Encyclopaedia") from e
            else:
                raise ValueError(
                    f"{entry} cannot be set because it is locked and 'show_locked_entry' is False",
                ) from e

        self.current_position = target_position

        self.active = entry
        self._change_active_entry_viewed_status()

        # When sorting by Unread, setting an entry marks is as read.
        # Thus we have to resort the entries to ensure they appear in the
        # correct order.
        if self.sorting_mode == SortMode.UNREAD:
            self._sort_entries(entries=self.current_entries)

    def _change_entry(self, direction: Direction) -> bool:
        """Change the active entry by changing the index.

        This is relative to the current sorting.

        Args:
            direction: The direction to move.
        """
        test_position = self.current_position + direction.value

        # Boundary check
        if test_position < 0:
            return False

        if test_position >= len(self):
            return False

        # Update the current position.
        self.current_position += direction.value

        # Update the active entry.
        self.active = self.current_entry

        self._change_active_entry_viewed_status()

        # When changing an entry, the current entry page number is reset.
        self.active._unlocked_page_index = 0

        return True

    def previous_entry(self) -> bool:
        """Set the previous entry as the current entry."""
        return self._change_entry(Direction.BACKWARD)

    def next_entry(self) -> bool:
        """Set the next entry as the current entry."""
        return self._change_entry(Direction.FORWARD)

    def PreviousEntry(self) -> PreviousEntry:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return PreviousEntry(self)

    def NextEntry(self) -> NextEntry:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return NextEntry(self)

    def PreviousPage(self) -> PreviousPage:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return PreviousPage(encyclopaedia=self)

    def NextPage(self) -> NextPage:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return NextPage(encyclopaedia=self)

    def Sort(self, sorting_mode: SortMode, reverse: bool = False) -> SortEncyclopaedia:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Args:
            sorting_mode: The type of sorting to use.
                If None specified, use the current sorting.
            reverse: Sort in reverse.

        Return:
            Screen Action
        """
        return SortEncyclopaedia(self, sorting_mode, reverse)

    def SetEntry(self, given_entry: 'EncEntry') -> SetEntry:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return SetEntry(self, given_entry)

    def CloseActiveEntry(self) -> CloseActiveEntry:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return CloseActiveEntry(self)

    def ResetSubPage(self) -> ResetSubPage:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return ResetSubPage(self)

    def ToggleShowLockedButtons(self) -> ToggleShowLockedButtonsAction:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return ToggleShowLockedButtonsAction(self)

    def ToggleShowLockedEntry(self) -> ToggleShowLockedEntryAction:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return ToggleShowLockedEntryAction(self)

    def FilterBySubject(self, subject: str) -> FilterBySubject:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return FilterBySubject(self, subject)

    def ClearFilter(self) -> ClearFilter:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return ClearFilter(self)
