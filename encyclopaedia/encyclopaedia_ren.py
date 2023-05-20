from typing import TYPE_CHECKING

from renpy import store

from .actions_ren import *  # NOQA: F403
from .actions_ren import (
    ClearFilter,
    FilterBySubject,
    NextEntry,
    PreviousEntry,
    NextPage,
    PreviousPage,
)
from .labels_ren import Labels
from .entry_sorting_ren import push_locked_to_bottom
from .eventemitter_ren import EventEmitter
from .constants_ren import Direction, SortMode

if TYPE_CHECKING:
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
        sorting_mode: The type of sorting used.
            Default sorting is by Number.
        show_locked_buttons: If True, locked entries show a
            placeholder label on the listing screen.
        show_locked_entry: If True, locked entries can be viewed, but
            the data is hidden from view with a placeholder.
        entry_screen: The Ren'Py screen to display an open entry.

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
        sub_current_position: Index for the current sub-entry open.
            Starts at 1.
        labels: The current label controller.
        subjects: Collection of every subject.
        active: The currently open entry.
        locked_at_bottom: True if locked entries should appear at
            the bottom of the entry list or not.
    """

    def __init__(self,
                 sorting_mode: int = 0,
                 show_locked_buttons: bool = False,
                 show_locked_entry: bool = False,
                 entry_screen: str = "encyclopaedia_entry",
                 ) -> None:

        self.sorting_mode = SortMode(sorting_mode)
        self.default_sorting_mode = self.sorting_mode

        self.show_locked_buttons = show_locked_buttons
        self.show_locked_entry = show_locked_entry
        self.entry_screen = entry_screen

        self.all_entries: list['EncEntry'] = []
        self.unlocked_entries: list['EncEntry'] = []
        self.filtered_entries: list['EncEntry'] = []

        self.filtering: Union[bool, str] = False

        self.reverse_sorting: bool = False
        if self.sorting_mode == SortMode.REVERSE_ALPHABETICAL:
            self.reverse_sorting = True

        self.nest_alphabetical_sort: bool = True

        self.current_position: int = 0
        self.sub_current_position: int = 1

        self.labels: Labels = Labels(self)

        self.subjects: list[str] = []

        self.active: Optional['EncEntry'] = None
        self._current_entries = self.all_entries

        self.locked_at_bottom: bool = True

        self.callbacks: dict[str, list[Callable[['Encyclopaedia'], None]]] = {
            "entry_unlocked": [],  # Run whenever a child entry is unlocked.
        }

    def __repr__(self) -> str:
        return f"<Encyclopaedia: {len(self.all_entries)} entries>"

    def __str__(self) -> str:
        return f"<Encyclopaedia: {len(self.all_entries)} entries>"

    @property
    def current_entries(self) -> list['EncEntry']:
        """Get all the entries which should be visible to the user.

        Return:
            List of EncEntries. If filtering, only entries that match the
            filter are returned.
        """
        if self.filtering:
            current_entries = self.filtered_entries
        elif self.show_locked_buttons:
            current_entries = self.all_entries
        else:
            current_entries = self.unlocked_entries

        return current_entries

    @current_entries.setter
    def current_entries(self, item: list['EncEntry']) -> None:
        self._current_entries = item

    @property
    def current_entry(self) -> 'EncEntry':
        """Get the entry at current_position.

        If show locked entries, pull from all_entries.
        Else, pull from unlocked_entries.

        Return:
            EncEntry
        """
        if self.show_locked_entry:
            entry = self.all_entries[self.current_position]
        else:
            entry = self.unlocked_entries[self.current_position]

        return entry

    @property
    def percentage_unlocked(self) -> float:
        """Get the percentage of the Encyclopaedia that's unlocked.

        Return:
            float: Percentage of the Encyclopaedia that's unlocked

        Raises:
            ZeroDivisionError: If the Encyclopaedia is empty
        """
        float_size = len(self.unlocked_entries)
        float_size_all = len(self.all_entries)

        try:
            amount_unlocked = float_size / float_size_all
        except ZeroDivisionError:
            raise ZeroDivisionError(
                'Cannot calculate percentage unlocked of empty Encyclopaedia'
            )

        percentage = floor(amount_unlocked * 100)
        return percentage

    @property
    def number_of_visible_entries(self) -> int:
        """Whatever the maximum size of the entry list should be,
        based on if locked entries should be shown or not.
        """
        if self.show_locked_entry:
            return len(self.all_entries)
        return len(self.unlocked_entries)

    def set_global_locked_name(self, placeholder: str) -> None:
        """Set all the locked names for all entries to the same string.

        Args:
            placeholder: Text to use for every locked name
        """
        for item in self.all_entries:
            item.locked_name = placeholder

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
            reverse=self.reverse_sorting
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
            reverse=self.reverse_sorting
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
        # Boundary check
        if self.current_position < 0:
            return False

        elif self.current_position >= self.number_of_visible_entries - 1:
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

        # When changing an entry, the current sub-entry page number is
        # set back to 1.
        self.sub_current_position = 0
        self.active.current_page = self.sub_current_position

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

    def Sort(self, sorting_mode: SortMode):  # NOQA: F405
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Args:
            sorting_mode: The type of sorting to use.
                If None specified, use the current sorting.

        Return:
            Screen Action
        """
        return SortEncyclopaedia(self, sorting_mode)  # NOQA: F405

    def SetEntry(self, given_entry: 'EncEntry'):
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return SetEntryAction(self, given_entry)  # NOQA: F405

    def ResetSubPage(self):
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return ResetSubPageAction(self)  # NOQA: F405

    def ToggleShowLockedButtons(self):
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return ToggleShowLockedButtonsAction(self)  # NOQA: F405

    def ToggleShowLockedEntry(self):
        """Wrapper around the Action of the same name.

        Use with a renpy button.

        Return:
            Screen Action
        """
        return ToggleShowLockedEntryAction(self)  # NOQA: F405

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