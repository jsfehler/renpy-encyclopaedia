# Copyright 2015 Joshua Fehler <jsfehler@gmail.com>
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

from math import floor
import operator

import renpy.store as store

import actions
from entrylist import EntryList
from labelcontroller import LabelController


class Encyclopaedia(store.object): 
    """
    Container that manages the display and sorting of a group of EncEntries.
    """
    
    # Constants for the different types of sorting available.
    SORT_NUMBER = 0
    SORT_ALPHABETICAL = 1
    SORT_REVERSE_ALPHABETICAL = 2
    SORT_SUBJECT = 3
    SORT_UNREAD = 4
            
    def __init__(self,
                 sorting_mode=0,
                 show_locked_buttons=False,
                 show_locked_entry=False,
                 show_locked_subjects=False,
                 entry_screen=''):
        # If True, locked entries show a placeholder label on
        # the listing screen.
        self.show_locked_buttons = show_locked_buttons

        # If True, locked entries can be viewed,
        # but the data is hidden from view with a placeholder
        # (defined in the EncEntry)
        self.show_locked_entry = show_locked_entry

        self.show_locked_subjects = show_locked_subjects

        # The screen to display an open entry
        self.entry_screen = entry_screen

        # List of all subjects
        self.all_subjects = []

        # List of unlocked subjects
        self.unlocked_subjects = []

        # List of all entries
        self.all_entries = EntryList()

        # List of unlocked entries
        self.unlocked_entries = EntryList()

        # Length of self.unlocked_entries        
        self._size = 0  
        
        # Length of self.all_entries
        self._size_all = 0  
        
        # The type of sorting used. Default sorting is by Number.
        self.sorting_mode = sorting_mode

        self.reverseSorting = False
        if sorting_mode == self.SORT_REVERSE_ALPHABETICAL:
            self.reverseSorting = True

        # Returns the currently open entry
        self.active = None
        
        # Pointer for the current entry open.
        # The current position based on the unlocked list.
        self.current_position = 0
        
        # The default sub-entry position is 1 because
        # the parent entry is the first page in the sub-entry list
        self.sub_current_position = 1

        # Load the default (English) label controller
        self.labels = LabelController(self)

    def __str__(self):
        return "Encyclopaedia"        

    @property
    def percentage_unlocked(self):
        """
        Returns:
            float - Percentage of the Encyclopaedia that's unlocked
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
                    
    def set_global_locked_image_tint(self, tint_amount):
        """
        Sets all the locked images in an Encyclopaedia to use the same tint.
        
        Parameters:
            tint_amount: tuple containing an RGB value (R, G, B)
        """
        for item in self.all_entries:
            item[1].tint_locked_image(
                (tint_amount[0], tint_amount[1], tint_amount[2])
            )
        
    def unlock_entry(self, entry, unlock_flag):
        """
        Unlocks an EncEntry and adds it to the list of unlocked entries.
        
        Returns:
            Entry that was unlocked
        """
        entry.locked = unlock_flag
        self.add_entry(entry)
        return entry

    def sort_entries(self, sorting=None, reverse=False):
        """
        Sort both entry lists by whatever the current sorting mode is.
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
    def check_position(op, current_position, value):
        """
        Checks the current_position against the min/max value of
        the Encyclopaedia.
        Used to determine if the Prev/Next Actions should be active.

        Returns:
            boolean
        """
        operators = {
            '<=': operator.le,
            '>=': operator.ge
        }

        if operators[op](current_position, value):
            return True
        return False

    def add_entry(self, item):
        """
        Adds an entry to the Encyclopaedia's internal lists and sorts it.
        The entry's subject is added to the subject lists.
        Attempts to create duplicates are softly ignored.
        """
        if item not in self.all_entries:
            self.all_entries.append(item)

        if item not in self.unlocked_entries and item.locked is False:
            self.unlocked_entries.append(item)

        # Sorting mode should be respected when adding entries
        self.sort_entries(
            sorting=self.sorting_mode,
            reverse=self.reverseSorting
        )

        # Update variables used for reporting
        self._size = len(self.unlocked_entries)
        self._size_all = len(self.all_entries)

        self.add_subject_from_entry(item)

    def add_entries(self, *new_entries):
        """
        Adds multiple new entries at once.
        """
        for item in new_entries:
            self.add_entry(item)

    def add_subject_from_entry(self, entry):
        """
        Adds a new subject to the Encyclopaedia from an Entry's subject
        attribute.
        Attempts to create duplicate subjects are softly ignored.
        """
        subject = entry.subject

        if subject not in self.all_subjects:
            self.all_subjects.append(subject)

        if subject not in self.unlocked_subjects and entry.locked is False:
            self.unlocked_subjects.append(subject)

    def PreviousEntry(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangeEntryAction(
            self,
            -1,
            self.check_position(
                '<=',
                self.current_position,
                0
            )
        )

    def NextEntry(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangeEntryAction(
            self,
            1,
            self.check_position(
                '>=',
                self.current_position,
                self.max_size - 1
            )
        )

    def PreviousPage(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangePageAction(
            self,
            -2,
            -1,
            self.check_position(
                '<=',
                self.sub_current_position,
                1
            )
        )

    def NextPage(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangePageAction(
            self,
            0,
            1,
            self.check_position(
                '>=',
                self.sub_current_position,
                self.active.pages
            )
        )

    def Sort(self, sorting_mode=None):
        """        
        Parameters: 
            sorting_mode: The type of sorting to use.
                If None specified, use the current sorting.
        
        Returns:
            Screen Action. Use with a button
        """
        if sorting_mode is None:
            sorting_mode = self.sorting_mode
        return actions.SortEncyclopaedia(self, sorting_mode)

    def SetEntry(self, given_entry):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.SetEntryAction(self, given_entry)

    def SaveStatus(self, enc_dict, tag_string):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.SaveStatusAction(self, enc_dict, tag_string)


    def ResetSubPage(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ResetSubPageAction(self)

    def ToggleShowLockedButtons(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ToggleShowLockedButtonsAction(self)

    def ToggleShowLockedEntry(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ToggleShowLockedEntryAction(self)
