from math import floor
import operator

import renpy.store as store

import actions
from entrylist import EntryList
from labelcontroller import LabelController


class Encyclopaedia(store.object): 
    """
    Container that manages the data for a group of EncEntries.
    """
    # Constants for the different types of sorting available.
    SORT_NUMBER = 0
    SORT_ALPHABETICAL = 1
    SORT_REVERSE_ALPHABETICAL = 2
    SORT_SUBJECT = 3
    SORT_UNREAD = 4

    # Constants for the direction when scrolling through EncEntry
    DIRECTION_FORWARD = 1
    DIRECTION_BACKWARD = -1
            
    def __init__(self,
                 sorting_mode=0,
                 show_locked_buttons=False,
                 show_locked_entry=False,
                 entry_screen=''):
        # Boolean: If True, locked entries show a placeholder label on
        #   the listing screen.
        self.show_locked_buttons = show_locked_buttons

        # Boolean: If True, locked entries can be viewed, but
        #   the data is hidden from view with a placeholder.
        self.show_locked_entry = show_locked_entry

        # String: The Ren'Py screen to display an open entry.
        self.entry_screen = entry_screen

        # List: Stores all entries.
        self.all_entries = EntryList()

        # List: Stores unlocked entries.
        self.unlocked_entries = EntryList()

        # Integer: Length of self.unlocked_entries.
        self._size = 0  
        
        # Integer: Length of self.all_entries.
        self._size_all = 0  
        
        # Integer: The type of sorting used. Default sorting is by Number.
        self.sorting_mode = sorting_mode

        # Boolean: When displaying Alphabetical sorted entries, should
        #   the letter be displayed before the entries?
        self.nest_alphabetical_sort = True

        # Boolean: Should we sort in reverse or not?
        self.reverse_sorting = False
        if sorting_mode == self.SORT_REVERSE_ALPHABETICAL:
            self.reverse_sorting = True

        # EncEntry: The currently open entry.
        self.active = None
        
        # Integer: Pointer for the current entry open.
        #   The current position based on the unlocked list.
        self.current_position = 0
        
        # Integer: The default sub-entry position is 1 because
        #   the parent entry is the first page in the sub-entry list.
        self.sub_current_position = 1

        # LabelController: Stores the default (English) label controller
        self.labels = LabelController(self)

    def __str__(self):
        return "Encyclopaedia"        

    @property
    def percentage_unlocked(self):
        """
        Returns:
            float: Percentage of the Encyclopaedia that's unlocked
        """
        float_size = float(self._size)
        float_size_all = float(self._size_all)

        try:
            amount_unlocked = float_size / float_size_all
        except ZeroDivisionError:
            raise ZeroDivisionError(
                'Cannot display percentage unlocked of empty Encyclopaedia'
            )

        percentage = floor(amount_unlocked * 100)
        return percentage

    @property
    def entry_list_size(self):
        """
        Returns:
            Whatever the current size of the entry list should be,
            based on if locked buttons should be shown or not
        """
        if self.show_locked_buttons:
            return self._size_all
        return self._size            

    @property
    def max_size(self):
        """
        Returns:
            Whatever the maximum size of the entry list should be,
            based on if locked buttons should be shown or not
        """
        if self.show_locked_entry:
            return self._size_all
        return self._size

    def set_global_locked_name(self, placeholder):
        """
        Sets all the locked names for all entries to the same string.

        Parameters:
            placeholder (str): Text to use for every locked name
        """
        for item in self.all_entries:
            item.locked_name = placeholder

    def set_global_locked_image_tint(self, tint_amount):
        """
        Sets all the locked images for all entries to use the same tint.
        
        Parameters:
            tint_amount (tuple): An RGB value, ie:(R, G, B)
        """
        for item in self.all_entries:
            item[1].tint_locked_image(
                (tint_amount[0], tint_amount[1], tint_amount[2])
            )

    def unlock_entry(self, entry, unlock_flag):
        """
        Unlocks an EncEntry and adds it to the list of unlocked entries.

        Parameters:
            entry (EncEntry): The Entry to unlock
            unlock_flag (bool): The variable that was associated with the locked
                parameter of the entry
        """
        entry.locked = unlock_flag

        # Run entry through add_entry() to add it to unlocked_entries
        self.add_entry(entry)

    def sort_entries(self, sorting=None, reverse=False):
        """
        Sort both entry lists by whatever the current sorting mode is.

        Parameters:
            sorting (int): The sorting mode to use
            reverse (bool): If the sorting should be done in reverse or not
        """
        if sorting == self.SORT_NUMBER:
            self.all_entries.sort_by_number()
            self.unlocked_entries.sort_by_number()
        elif sorting == self.SORT_UNREAD:
            self.all_entries.sort_by_unread()
            self.unlocked_entries.sort_by_unread()
        else:
            self.all_entries.sort_by_name(reverse=reverse)
            self.unlocked_entries.sort_by_name(reverse=reverse)

    @staticmethod
    def check_position(op, position, wall):
        """
        Checks the current_position against the min/max value of
        the Encyclopaedia.
        Used to determine if the Prev/Next Actions should be active.

        Parameters:
            op (str): The operator to use
            position (int): The position of the entry
            wall (int): The limit to check against

        Returns:
            bool
        """
        operators = {
            '<=': operator.le,
            '>=': operator.ge
        }

        if operators[op](position, wall):
            return True
        return False

    def add_entry(self, entry):
        """
        Adds an entry to the Encyclopaedia's internal lists and sorts it.
        The entry's subject is added to the subject lists.
        Attempts to create duplicates are softly ignored.

        Parameters:
            entry (EncEntry): The Entry to add to the Encyclopaedia

        """
        if entry not in self.all_entries:
            self.all_entries.append(entry)

        if entry not in self.unlocked_entries and entry.locked is False:
            self.unlocked_entries.append(entry)

        # Sorting mode should be respected when adding entries
        self.sort_entries(
            sorting=self.sorting_mode,
            reverse=self.reverse_sorting
        )

        # Update variables used for reporting
        self._size = len(self.unlocked_entries)
        self._size_all = len(self.all_entries)

    def add_entries(self, *new_entries):
        """
        Adds multiple new entries at once.
        """
        for item in new_entries:
            self.add_entry(item)

    def PreviousEntry(self):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '<=',
            position=self.current_position,
            wall=0
        )

        return actions.ChangeEntryAction(
            encyclopaedia=self,
            direction=self.DIRECTION_BACKWARD,
            block=block
        )

    def NextEntry(self):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '>=',
            position=self.current_position,
            wall=self.max_size - 1
        )

        return actions.ChangeEntryAction(
            encyclopaedia=self,
            direction=self.DIRECTION_FORWARD,
            block=block
        )

    def PreviousPage(self):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '<=',
            position=self.sub_current_position,
            wall=1
        )

        return actions.ChangePageAction(
            encyclopaedia=self,
            direction=self.DIRECTION_BACKWARD,
            block=block
        )

    def NextPage(self):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        block = self.check_position(
            '>=',
            position=self.sub_current_position,
            wall=self.active.pages
        )

        return actions.ChangePageAction(
            encyclopaedia=self,
            direction=self.DIRECTION_FORWARD,
            block=block
        )

    def Sort(self, sorting_mode=None):
        """
        Use with a renpy button.

        Parameters: 
            sorting_mode: The type of sorting to use.
                If None specified, use the current sorting.
        
        Returns:
            Screen Action
        """
        if sorting_mode is None:
            sorting_mode = self.sorting_mode
        return actions.SortEncyclopaedia(self, sorting_mode)

    def SetEntry(self, given_entry):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        return actions.SetEntryAction(self, given_entry)

    def SaveStatus(self, enc_dict, tag_string):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        return actions.SaveStatusAction(self, enc_dict, tag_string)

    def ResetSubPage(self):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        return actions.ResetSubPageAction(self)

    def ToggleShowLockedButtons(self):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        return actions.ToggleShowLockedButtonsAction(self)

    def ToggleShowLockedEntry(self):
        """
        Use with a renpy button.

        Returns:
            Screen Action
        """
        return actions.ToggleShowLockedEntryAction(self)
