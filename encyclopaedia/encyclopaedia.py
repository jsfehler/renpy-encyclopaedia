from math import floor
import operator
from operator import attrgetter

from renpy import store

from .actions import *  # NOQA: F403
from .labels import Labels
from .entry_sorting import push_locked_to_bottom
from .eventemitter import EventEmitter


class Encyclopaedia(EventEmitter, store.object):
    """Container that manages the behaviour of a collection of EncEntry objects.

    Args:
        sorting_mode (int): The type of sorting used.
            Default sorting is by Number.
        show_locked_buttons (bool): If True, locked entries show a
            placeholder label on the listing screen.
        show_locked_entry (bool): If True, locked entries can be viewed, but
            the data is hidden from view with a placeholder.
        entry_screen (str): The Ren'Py screen to display an open entry.

    Attributes:
        all_entries (list): All entries, regardless of status.
        unlocked_entries (list): Only unlocked entries.
        filtered_entries (list): Entries that match a subject filter.
        filtering (bool|str): The subject that's being used as a filter.
        size_all (int): Length of self.all_entries.
        size_unlocked (int): Length of self.unlocked_entries.
        reverse_sorting (bool): Should sorting occur in reverse or not.
        nest_alphabetical_sort (bool): Should alphabetical sorting display
            each letter as a subject.
        current_position (int): Index for the current entry open.
        sub_current_position (int): Index for the current sub-entry open.
            Starts at 1.
        labels (Labels): The current label controller.
        subjects (list): Collection of every subject.
        active (EncEntry): The currently open entry.
        locked_at_bottom (bool): If locked entries should appear at the bottom
            of the entry list or not.
    """
    # Constants for the different types of sorting available.
    SORT_NUMBER = 0
    SORT_ALPHABETICAL = 1
    SORT_REVERSE_ALPHABETICAL = 2
    SORT_SUBJECT = 3
    SORT_UNREAD = 4

    # Constants for the direction when scrolling through EncEntry.
    DIRECTION_FORWARD = 1
    DIRECTION_BACKWARD = -1

    # Used by check_position().
    operators = {'<=': operator.le, '>=': operator.ge}

    def __init__(self,
                 sorting_mode=0,
                 show_locked_buttons=False,
                 show_locked_entry=False,
                 entry_screen="encyclopaedia_entry",
                 tint_locked_image=True):

        self.sorting_mode = sorting_mode
        self.default_sorting_mode = sorting_mode
        self.show_locked_buttons = show_locked_buttons
        self.show_locked_entry = show_locked_entry
        self.entry_screen = entry_screen

        self.tint_locked_image = tint_locked_image

        self.all_entries = []
        self.unlocked_entries = []
        self.filtered_entries = []

        self.filtering = False

        self._size_all = 0
        self._size_unlocked = 0

        self.reverse_sorting = False
        if sorting_mode == self.SORT_REVERSE_ALPHABETICAL:
            self.reverse_sorting = True

        self.nest_alphabetical_sort = True

        self.current_position = 0
        self.sub_current_position = 1

        self.labels = Labels(self)

        self.subjects = []

        self.active = None
        self._current_entries = self.all_entries

        self.locked_at_bottom = True

        self.callbacks = {
            "unlock": [],  # Run whenever a child entry is unlocked.
        }

    def __str__(self):
        return "Encyclopaedia: {} entries total".format(self._size_all)

    @property
    def current_entries(self):
        return self._current_entries

    @current_entries.getter
    def current_entries(self):
        """list: Depending on which viewing options are set,
        returns a list of entries.
        """
        if self.filtering:
            current_entries = self.filtered_entries
        elif self.show_locked_buttons:
            current_entries = self.all_entries
        else:
            current_entries = self.unlocked_entries

        return current_entries

    @current_entries.setter
    def current_entries(self, item):
        self._current_entries = item

    @property
    def percentage_unlocked(self):
        """Gets the percentage of the Encyclopaedia that's unlocked.

        Returns:
            float: Percentage of the Encyclopaedia that's unlocked

        Raises:
            ZeroDivisionError: If the Encyclopaedia is empty
        """
        float_size = float(self._size_unlocked)
        float_size_all = float(self._size_all)

        try:
            amount_unlocked = float_size / float_size_all
        except ZeroDivisionError:
            raise ZeroDivisionError(
                'Cannot calculate percentage unlocked of empty Encyclopaedia'
            )

        percentage = floor(amount_unlocked * 100)
        return percentage

    @property
    def number_of_visible_entries(self):
        """int: Whatever the maximum size of the entry list should be,
        based on if locked entries should be shown or not.
        """
        if self.show_locked_entry:
            return self._size_all
        return self._size_unlocked

    def set_global_locked_name(self, placeholder):
        """Sets all the locked names for all entries to the same string.

        Args:
            placeholder (str): Text to use for every locked name
        """
        for item in self.all_entries:
            item.locked_name = placeholder

    def set_global_locked_image_tint(self, tint_amount):
        """Sets all the locked images for all entries to use the same tint.

        Args:
            tint_amount (tuple): An RGB value, ie:(R, G, B)
        """
        for item in self.all_entries:
            item[1].tint_locked_image(
                (tint_amount[0], tint_amount[1], tint_amount[2])
            )

    def sort_entries(self, entries, sorting=0, reverse=False):
        """Sort entry lists by whatever the current sorting mode is.

        Args:
            entries (list): The entry list to sort
            sorting (int): The sorting mode to use
            reverse (bool): If the sorting should be done in reverse or not
        """
        if sorting == self.SORT_NUMBER:
            entries.sort(key=attrgetter('number'))
        else:
            entries.sort(reverse=reverse, key=attrgetter('name'))

            if sorting == self.SORT_UNREAD:
                entries.sort(key=attrgetter('viewed'))

            elif sorting == self.SORT_SUBJECT:
                entries.sort(key=attrgetter('subject'))

            if self.locked_at_bottom:
                push_locked_to_bottom(entries)

    def check_position(self, op, position, wall):
        """Determines if the Prev/Next Actions should be active or not.

        Args:
            op (str): The operator to use
            position (int): The position of the entry
            wall (int): The limit to check against

        Returns:
            bool
        """
        if self.operators[op](position, wall):
            return True
        return False

    def add_entry_to_unlocked_entries(self, entry):
        """Adds an entry to the list of unlocked entries.

        Args:
            entry (EncEntry): The Entry to add to the unlocked entries list.
        """

        self.unlocked_entries.append(entry)

        # Remove duplicates
        self.unlocked_entries = list(set(self.unlocked_entries))

        self.sort_entries(
            entries=self.unlocked_entries,
            sorting=self.sorting_mode,
            reverse=self.reverse_sorting
        )

        self._size_unlocked = len(self.unlocked_entries)

    def add_entry(self, entry):
        """Adds an entry to the Encyclopaedia's internal lists and sorts it.

        Attempts to create duplicates are softly ignored.
        subjects list is updated when a new entry is added.

        Args:
            entry (EncEntry): The Entry to add to the Encyclopaedia
        """
        if entry.parent is not None and entry.parent != self:
            raise ValueError(
                "{} is already inside another Encyclopaedia".format(entry),
            )

        # When a new entry has a number, ensure it's not already used.
        if entry.number is not None:
            if any(i for i in self.all_entries if i.number == entry.number):
                raise ValueError(
                    "{} is already taken.".format(entry.number)
                )

        elif entry.number is None:
            if self._size_all > 0:
                # All possible numbers
                all_numbers = range(self.all_entries[-1].number + 1)[1:]
                used_numbers = [item.number for item in self.all_entries]
                free_numbers = set(all_numbers) - set(used_numbers)

                if len(free_numbers) > 0:
                    # If there are unused numbers.
                    entry.number = min(free_numbers)
                else:
                    # Else the entry is the last one.
                    entry.number = self._size_all + 1
            else:
                # If there's no entries in the Encyclopaedia yet.
                entry.number = 1

        self.all_entries.append(entry)
        entry.parent = self

        # Ensure no duplicates in the entry lists.
        self.all_entries = list(set(self.all_entries))

        # Ensure correct sorting of entry lists.
        self.sort_entries(
            entries=self.all_entries,
            sorting=self.sorting_mode,
            reverse=self.reverse_sorting
        )

        self._size_all = len(self.all_entries)

        if entry.locked is False:
            self.add_entry_to_unlocked_entries(entry)

        self.subjects.append(entry.subject)
        self.subjects = list(set(self.subjects))
        self.subjects.sort()

    def PreviousEntry(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '<=',
            position=self.current_position,
            wall=0
        )

        return ChangeEntryAction(  # NOQA: F405
            encyclopaedia=self,
            direction=self.DIRECTION_BACKWARD,
            block=block
        )

    def NextEntry(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '>=',
            position=self.current_position,
            wall=self.number_of_visible_entries - 1
        )

        return ChangeEntryAction(  # NOQA: F405
            encyclopaedia=self,
            direction=self.DIRECTION_FORWARD,
            block=block
        )

    def PreviousPage(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '<=',
            position=self.sub_current_position,
            wall=1
        )

        return ChangePageAction(  # NOQA: F405
            encyclopaedia=self,
            direction=self.DIRECTION_BACKWARD,
            block=block
        )

    def NextPage(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '>=',
            position=self.sub_current_position,
            wall=self.active.pages
        )

        return ChangePageAction(  # NOQA: F405
            encyclopaedia=self,
            direction=self.DIRECTION_FORWARD,
            block=block
        )

    def Sort(self, sorting_mode=None):  # NOQA: F405
        """Wrapper around an Action. Use with a renpy button.

        Args:
            sorting_mode: The type of sorting to use.
                If None specified, use the current sorting.

        Returns:
            Screen Action
        """
        if sorting_mode is None:
            sorting_mode = self.sorting_mode

        return SortEncyclopaedia(self, sorting_mode)  # NOQA: F405

    def SetEntry(self, given_entry):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        return SetEntryAction(self, given_entry)  # NOQA: F405

    def ResetSubPage(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        return ResetSubPageAction(self)  # NOQA: F405

    def ToggleShowLockedButtons(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        return ToggleShowLockedButtonsAction(self)  # NOQA: F405

    def ToggleShowLockedEntry(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        return ToggleShowLockedEntryAction(self)  # NOQA: F405

    def FilterBySubject(self, subject):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        return FilterBySubject(self, subject)  # NOQA: F405

    def ClearFilter(self):
        """Wrapper around an Action. Use with a renpy button.

        Returns:
            Screen Action
        """
        return ClearFilter(self)  # NOQA: F405
