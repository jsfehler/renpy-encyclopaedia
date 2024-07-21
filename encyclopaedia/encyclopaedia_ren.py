from typing import TYPE_CHECKING

from renpy import store

from .actions_ren import (
    ClearFilter,
    CloseActiveEntry,
    FilterBySubject,
    NextEntry,
    PreviousEntry,
    NextPage,
    PreviousPage,
    SortEncyclopaedia,
    SetEntry,
    ResetSubPage,
    ToggleShowLockedButtonsAction,
    ToggleShowLockedEntryAction,
)
from .entry_sorting_ren import push_locked_to_bottom
from .eventemitter_ren import EventEmitter
from .constants_ren import Direction, SortMode

if TYPE_CHECKING:  # pragma: no cover
    from .encentry_ren import EncEntry

"""renpy
init python:
"""
from math import floor  # NOQA E402
from operator import attrgetter  # NOQA E402
from typing import cast, Callable, Optional, Union  # NOQA E402


class Encyclopaedia(EventEmitter, store.object):
    """Container that manages the behaviour of a collection of EncEntry objects.

    Args:
        sorting_mode: The default for how entries are sorted.
            Default sorting is by Number.
        show_locked_buttons: If True, locked entries show a
            placeholder label on the listing screen.
        show_locked_entry: If True, locked entries can be viewed, but
            the data is hidden from view with a placeholder.
        list_screen: The Ren'Py screen to display the list of entries.
        entry_screen: The Ren'Py screen to display an open entry.
        name: A optional name for the Encyclopaedia.

    Attributes:
        all_entries: All entries, regardless of status.
        unlocked_entries: Only unlocked entries.
        filtered_entries: Entries that match a subject filter.
        filtering: The subject that's being used as a filter.
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
                 sorting_mode: int = 0,
                 show_locked_buttons: bool = False,
                 show_locked_entry: bool = False,
                 list_screen: str = 'encyclopaedia_list',
                 entry_screen: str = 'encyclopaedia_entry',
                 name: str = '',
                 ) -> None:

        self.sorting_mode = SortMode(sorting_mode)
        self.show_locked_buttons = show_locked_buttons
        self.show_locked_entry = show_locked_entry
        self.list_screen = list_screen
        self.entry_screen = entry_screen
        self.name = name

        self.all_entries: list['EncEntry'] = []
        self.unlocked_entries: list['EncEntry'] = []
        self.filtered_entries: list['EncEntry'] = []

        self.filtering: Union[bool, str] = False

        self.reverse_sorting: bool = False
        if self.sorting_mode == SortMode.REVERSE_ALPHABETICAL:
            self.reverse_sorting = True

        self.nest_alphabetical_sort: bool = True

        self.current_position: int = 0

        self.subjects: list[str] = []

        self.active: Optional['EncEntry'] = None
        self._current_entries = self.all_entries

        self.locked_at_bottom: bool = True

        self.callbacks: dict[str, list[Callable[['Encyclopaedia'], None]]] = {
            "entry_unlocked": [],  # Run whenever a child entry is unlocked.
        }

    def __repr__(self) -> str:  # NOQA D105
        return f"Encyclopaedia(name={self.name}, length={len(self.all_entries)})"

    def __str__(self) -> str:  # NOQA D105
        return f"Encyclopaedia: {self.name}"

    def __len__(self) -> int:
        """The total number of entries, relative to if locked ones are shown or not."""
        rv = len(self.unlocked_entries)
        if self.show_locked_entry:
            rv = len(self.all_entries)

        return rv

    @property
    def current_entries(self) -> list['EncEntry']:
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
    def current_entry(self) -> 'EncEntry':
        """Get the entry at current_position.

        If show locked entries, pull from all_entries.
        Else, pull from unlocked_entries.

        Return:
            EncEntry
        """
        entry = self.unlocked_entries[self.current_position]
        if self.show_locked_entry:
            entry = self.all_entries[self.current_position]

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

    def sort_entries(
        self,
        entries: list['EncEntry'],
        sorting: int = 0,
        reverse: bool = False,
    ) -> None:
        """Sort entry lists by whatever the current sorting mode is.

        Args:
            entries: The EncEntry list to sort
            sorting: The sorting mode to use
            reverse: If the sorting should be done in reverse or not
        """
        sorting_mode = SortMode(sorting)

        if sorting_mode == SortMode.NUMBER:
            entries.sort(key=attrgetter('number'))
        else:
            entries.sort(reverse=reverse, key=attrgetter('name'))

            if sorting_mode == SortMode.UNREAD:
                entries.sort(key=attrgetter('viewed'))

            elif sorting_mode == SortMode.SUBJECT:
                entries.sort(key=attrgetter('subject'))

            if self.locked_at_bottom:
                push_locked_to_bottom(entries)

    def add_entry_to_unlocked_entries(self, entry: 'EncEntry') -> None:
        """Add an entry to the list of unlocked entries.

        Args:
            entry: The Entry to add to the unlocked entries list.
        """
        self.unlocked_entries.append(entry)

        # Remove duplicates
        self.unlocked_entries = list(set(self.unlocked_entries))

        self.sort_entries(
            entries=self.unlocked_entries,
            sorting=int(self.sorting_mode.value),
            reverse=self.reverse_sorting,
        )

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

    def add_entry(self, entry: 'EncEntry') -> None:
        """Add an entry to the Encyclopaedia's internal lists and sorts it.

        Attempts to create duplicates are softly ignored.
        subjects list is updated when a new entry is added.

        Args:
            entry: The Entry to add to the Encyclopaedia
        """
        if entry.parent is not None and entry.parent != self:
            raise ValueError(
                f"{entry} is already inside another Encyclopaedia",
            )

        # When a new entry has a number, ensure it's not already used.
        if entry.number is not None:
            if any(i for i in self.all_entries if i.number == entry.number):
                raise ValueError(f"{entry.number} is already taken.")

        elif entry.number is None:
            entry.number = self._find_closest_free_number()

        self.all_entries.append(entry)
        entry.parent = self

        # Ensure no duplicates in the entry lists.
        self.all_entries = list(set(self.all_entries))

        # Ensure correct sorting of entry lists.
        self.sort_entries(
            entries=self.all_entries,
            sorting=int(self.sorting_mode.value),
            reverse=self.reverse_sorting,
        )

        if entry.locked is False:
            self.add_entry_to_unlocked_entries(entry)

        self.subjects.append(entry.subject)
        self.subjects = list(set(self.subjects))
        self.subjects.sort()

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

    def _change_entry(self, direction: Direction) -> bool:
        """Change the current active EncEntry."""
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

        if self.active.locked is False:
            # Run the callback, if provided.
            self.active.emit("viewed")

            # Mark the entry as viewed.
            self.active.viewed = True

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

    def Sort(self, sorting_mode: SortMode) -> SortEncyclopaedia:
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Args:
            sorting_mode: The type of sorting to use.
                If None specified, use the current sorting.

        Return:
            Screen Action
        """
        return SortEncyclopaedia(self, sorting_mode)

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
