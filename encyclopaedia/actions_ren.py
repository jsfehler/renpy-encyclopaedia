from .constants_ren import SortMode

import renpy.exports as renpy
from renpy.store import DictEquality
from renpy.ui import Action

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .encyclopaedia_ren import Encyclopaedia
    from .encentry_ren import EncEntry

"""renpy
init python:
"""


class EncyclopaediaAction(Action, DictEquality):
    """Base Action that requires an Encyclopaedia as an argument.

    Should only be used for class inheritance.

    Args:
        encyclopaedia: The Encyclopaedia instance to use.
    """
    def __init__(self, encyclopaedia: 'Encyclopaedia') -> None:
        self.enc = encyclopaedia


class SetEntry(EncyclopaediaAction):
    """Set an Entry as active, then open the Encyclopaedia's Entry Screen.

    Generally used with Ren'py Button displayable to display an Entry.

    Args:
        encyclopaedia: The Encyclopaedia instance to use.
        entry: The entry to be made active.
    """
    def __init__(self, encyclopaedia: 'Encyclopaedia', entry: 'EncEntry') -> None:
        super().__init__(encyclopaedia)

        self.entry = entry

    def _get_entry_index(self) -> int:
        # Find the position of the entry
        if self.enc.show_locked_entry:
            target_position = self.enc.all_entries.index(self.entry)
        else:
            target_position = self.enc.unlocked_entries.index(self.entry)

        return target_position

    def set_entry(self) -> None:
        """Set the Entry as active and update the Encyclopaeda's internal state."""
        target_position = self._get_entry_index()

        # The active entry is set to whichever list position was found.
        self.enc.active = self.entry

        if self.enc.active.locked is False:
            if self.entry.viewed is False:
                # Run the callback, if provided.
                self.entry.emit("viewed")
            # Mark the entry as viewed.
            self.enc.active.viewed = True

        # When sorting by Unread, setting an entry marks is as read.
        # Thus we have to resort the entries to ensure they appear in the
        # correct order.
        if self.enc.sorting_mode.value == SortMode.UNREAD.value:
            self.enc.sort_entries(
                entries=self.enc.current_entries,
                sorting=self.enc.sorting_mode.value,
            )

        self.enc.current_position = target_position

    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        self.set_entry()

        # Show the entry screen associated with the encyclopaedia.
        renpy.show_screen(self.enc.entry_screen, enc=self.enc)
        renpy.restart_interaction()

    def get_sensitive(self) -> bool:
        """Check if the button this Action is attached to should be active or not.

        Return:
            True if locked entries can be displayed or the EncEntry is not
            locked, else False.
        """
        if self.enc.show_locked_entry or (not self.entry.locked):
            return True
        else:
            return False

    def get_selected(self) -> bool:
        """Used by Ren'Py to determine if the user of this Action should have a selected state.

        Returns:
            True if the Entry set by this Action is the active Entry, else False.
        """
        return self.entry == self.enc.active


class CloseActiveEntry(EncyclopaediaAction):
    """Close the active EncEntry.

    Normally used by the entry screen.
    """
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        self.enc.active = None
        self.enc.ResetSubPage()()
        renpy.hide_screen(self.enc.entry_screen)


class PreviousEntry(EncyclopaediaAction):
    """Change the current entry being viewed.

    Used to switch from one entry to another.

    Args:
        encyclopaedia: The Encyclopaedia instance to use.
    """
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        result = self.enc.previous_entry()

        if result:
            renpy.restart_interaction()

    def get_sensitive(self) -> bool:
        """Determine if the button should be alive or not.

        Return:
            True if the button should be alive, else False.
        """
        if not self.enc.active:
            return False

        return not (self.enc.current_position) <= 0


class NextEntry(EncyclopaediaAction):
    """Change the current entry being viewed.

    Used to switch from one entry to another.

    Args:
        encyclopaedia: The Encyclopaedia instance to use.
    """
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        result = self.enc.next_entry()

        if result:
            renpy.restart_interaction()

    def get_sensitive(self) -> bool:
        """Determine if the button should be alive or not.

        Return:
            True if the button should be alive, else False.
        """
        if not self.enc.active:
            return False

        return not (self.enc.current_position) >= (len(self.enc) - 1)


class PreviousPage(EncyclopaediaAction):
    """Change the current sub-entry being viewed.

    Used to switch from one page to another.
    """
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        active = self.enc.active

        if not active:
            raise AttributeError('Cannot change entry when no entry is set.')

        result = active.previous_page()

        if result:
            renpy.restart_interaction()

    def get_sensitive(self) -> bool:
        """Determine if the button should be alive or not.

        Return:
            bool: True if the button should be alive, else False.
        """
        active = self.enc.active

        if not active:
            return False

        return not (active._unlocked_page_index - 1) < 0


class NextPage(EncyclopaediaAction):
    """Change the current sub-entry being viewed.

    Used to switch from one page to another.
    """
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        active = self.enc.active

        if not active:
            raise AttributeError('Cannot change entry when no entry is set.')

        result = active.next_page()

        if result:
            renpy.restart_interaction()

    def get_sensitive(self) -> bool:
        """Determine if the button should be alive or not.

        Return:
            bool: True if the button should be alive, else False.
        """
        active = self.enc.active

        if not active:
            return False

        return not (active._unlocked_page_index + 1) >= len(active.unlocked_pages)


class SortEncyclopaedia(EncyclopaediaAction):
    """Sort the entries based on encyclopaedia.sorting_mode.

    Args:
        encyclopaedia: The Encyclopaedia instance to use.
        sorting_mode: The sorting mode to sort by.
    """
    def __init__(
        self,
        encyclopaedia: 'Encyclopaedia',
        sorting_mode: SortMode,
    ) -> None:
        super().__init__(encyclopaedia)

        self.sorting_mode = sorting_mode

        self.reverse = False
        if self.sorting_mode == SortMode.REVERSE_ALPHABETICAL:
            self.reverse = True

    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        self.enc.sort_entries(
            entries=self.enc.current_entries,
            sorting=int(self.sorting_mode.value),
            reverse=self.reverse,
        )

        self.enc.sorting_mode = self.sorting_mode
        renpy.restart_interaction()

    def get_selected(self) -> bool:
        """Used by Ren'Py to determine if the user of this Action should have a selected state.

        Returns:
            True if the Encyclopaedia's current sorting mode matches the one set
            by this Action, else False.
        """
        return self.enc.sorting_mode == self.sorting_mode


class FilterBySubject(EncyclopaediaAction):
    """Create a filter for entries, based on the given subject."""
    def __init__(self, encyclopaedia: 'Encyclopaedia', subject: str) -> None:
        super().__init__(encyclopaedia)

        self.subject = subject

    def __call__(self):
        """Used by Ren'Py to invoke this Action."""
        self.enc.filtering = self.subject

        self.enc._build_subject_filter(self.subject)

        renpy.restart_interaction()

    def get_selected(self) -> bool:
        """Used by Ren'Py to determine if the user of this Action should have a selected state.

        Returns:
            True if the Encyclopaedia is filtering and the filter matches the one set
            by this Action, else False.
        """
        self.selected = self.enc.filtering == self.subject
        return self.selected


class ClearFilter(EncyclopaediaAction):
    """Stop filtering an Encyclopaedia."""
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        self.enc.filtering = False
        renpy.restart_interaction()


class ResetSubPage(EncyclopaediaAction):
    """Reset the sub-page count to 1. Used when closing the entry screen."""
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        if self.enc.active is not None:
            self.enc.active._unlocked_page_index = 0
        renpy.restart_interaction()


class ToggleShowLockedButtonsAction(EncyclopaediaAction):
    """Toggle if locked Entries will be visible in the list of Entries."""
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        self.enc.show_locked_buttons = not self.enc.show_locked_buttons

        # Ensure the filtering isn't broken by hiding buttons.
        if isinstance(self.enc.filtering, str):
            self.enc._build_subject_filter(self.enc.filtering)

        # Ensure the sorting isn't broken by hiding buttons.
        reverse = False
        if self.enc.sorting_mode == SortMode.REVERSE_ALPHABETICAL:
            reverse = True

        self.enc.sort_entries(
            entries=self.enc.current_entries,
            sorting=int(self.enc.sorting_mode.value),
            reverse=reverse,
        )

        renpy.restart_interaction()


class ToggleShowLockedEntryAction(EncyclopaediaAction):
    """Toggle if locked Entries can be viewed."""
    def __call__(self) -> None:
        """Used by Ren'Py to invoke this Action."""
        self.enc.show_locked_entry = not self.enc.show_locked_entry
        renpy.restart_interaction()
