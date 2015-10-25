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

import renpy.store as store
import renpy.exports as renpy

import actions
from entrylist import EntryList
from labelcontroller import LabelController

persistent = renpy.game.persistent


class Encyclopaedia(store.object): 
    """ Container that manages the display and sorting of a group of EncEntries. """
    
    # Constants for the different types of sorting available.
    SORT_NUMBER = 0
    SORT_ALPHABETICALLY = 1
    SORT_REVERSE_ALPHABETICALLY = 2
    SORT_SUBJECT = 3
    SORT_UNREAD = 4
            
    def __init__(self,
                 sorting_mode=0,
                 show_locked_buttons=False,
                 show_locked_entry=False,
                 entry_screen=''):
        # List of all subjects
        self.subjects = []
        
        # List of unlocked entries
        self.unlocked_entries = EntryList()
        
        # List of all entries, regardless of if locked or not
        self.all_entries = EntryList() 
        
        # Length of self.unlocked_entries        
        self._size = 0  
        
        # Length of self.all_entries
        self._size_all = 0  
        
        # The type of sorting used. Default sorting is by Number.
        self.sorting_mode = sorting_mode

        self.reverseSorting = False
        if sorting_mode == self.SORT_REVERSE_ALPHABETICALLY:
            self.reverseSorting = True

        # If True, locked entries show a placeholder label on the listing screen.
        self.show_locked_buttons = show_locked_buttons
        
        # If True, locked entries can be viewed,
        # but the data is hidden from view with a placeholder (defined in the EncEntry)
        self.show_locked_entry = show_locked_entry

        # Returns the currently open entry
        self.active = None
        
        # Pointer for the current entry open. Is the current position based on the unlocked list.
        self.current_position = 0
        
        # The default sub-entry position is 1 because the parent entry is the first page in the sub-entry list
        self.sub_current_position = 1
        
        # The screen to display an open entry
        self.entry_screen = entry_screen
        
        # Load the default (English) label controller
        self.labels = LabelController(self)

    def __str__(self):
        return "Encyclopaedia"        
        
    @property
    def entry_list_size(self):
        """
        Returns:
            Whatever the current size of the entry list should be, based on if locked buttons should be shown or not.
        """
        if self.show_locked_buttons:
            return self._size_all
        return self._size            

    @property
    def max_size(self):
        """
        Returns:
            Whatever the maximum size of the entry list should be, based on if locked buttons should be shown or not.
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
        for item_number, item in self.all_entries:
            item.tint_locked_image((tint_amount[0], tint_amount[1], tint_amount[2]))        
        
    def unlock_entry(self, entry, unlock_flag):
        """
        Unlocks an EncEntry and adds it to the list of unlocked entries.
        
        Returns:
            Entry that was unlocked
        """
        entry.locked = unlock_flag
        self.addEntry(entry)
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
 
    def get_entry_at(self, entry_number): 
        """ 
        Used for displaying the buttons.
        Gets an entry from either all_entries or unlocked_entries
        Depends on if locked entries should be in the entry list or not.
        
        Parameters:
            entry_number: The list position for the desired entry.
        
        Returns: 
            The entry of the specified entry_number
        """
        if self.show_locked_buttons:
            return self.get_all_entry_at(entry_number)
        return self.get_unlocked_entry_at(entry_number)

    def get_all_entry_at(self, entry_number): 
        """
        Returns: 
            The entry associated with entry_number from all_entries list
        """
        return self.all_entries[entry_number]

    def get_unlocked_entry_at(self, entry_number): 
        """
        Returns:
            The entry associated with entry_number from unlocked_entries list
        """
        return self.unlocked_entries[entry_number]
        
    # Checks the current_position against the min or max of the encyclopaedia, returns Boolean
    # Used to determine if the Prev/Next Actions should be active
    def check_min(self, check_position, min_val):
        if check_position <= min_val:
            return True
        return False

    def check_max(self, check_position, max_val):
        if check_position >= max_val:
            return True
        return False
 
    def _make_persistent_dict(self, total, master_key, persistent_var_string):
        """
        For the total amount given,
            1) takes two strings to define a series of keys and values in a dictionary. 
            2) Creates two lists and evaluates the values to variables. 
            3) Then combines the lists into a dictionary.
        
        Parameters:
            total: The number of entries in the dictionary that's going to be made
            master_key: The prefix for the keys
            persistent_var_string: The string that will be turned into the variables for the values in the dictionary
            
        Returns:
            Dictionary with persistent values
        """

        # eg: new_00, new_01, etc
        keys = [master_key % x for x in range(total)]
                
        # eg: persistent.new_dict["new_00"], persistent.new_dict["new_01"], etc
        vals_string = [persistent_var_string % x for x in range(total)]
        # Eval strings into the actual variables
        vals = [eval(item) for item in vals_string]
        
        combo = zip(keys, vals)
        return dict(combo)  

    def setPersistentStatus(self, entries_total=0, master_key="new", name="new"):
        """
        Create the persistent status variables to manage the "New!" status if an Encyclopaedia is save game independent.
        This will create the variables, but it's up to you to use them in the "status" argument for an EncEntry.
        This function must always be called when the game starts.
        
        If you want a save game specific "New!" status, don't use persistent variables, 
        and create the EncEntry after the start label, not in an init block.
        
        How it works:
        Two dictionaries are created: persistent.<name>_vals and persistent.<name>_dict.
        master_key is the prefix for all the keys in both dictionaries.
        name is the prefix for the dictionary names.
        Both default to "new".
        
        When this function runs, each key in persistent.new_vals is given the value of an entry in 
        persistent.new_dict and vice versa.
        eg: persistent.new_vals["new_00"] = persistent.new_dict["new_00"]
            persistent.new_dict["new_00"] = persistent.new_dict["new_00"]
            
        Each EncEntry must use persistent.new_dict["new_<x>"] for their status variable.
            
        Why it works:
        If the value is None or False, "New!" is displayed.
        As each entry is opened and exited, the value in new_dict is set to True.
        
        Each time the game is started, new_vals is set to whatever the matching new_dict value is.
        new_dict then sets itself to whatever new_vals is.
        
        The reason this is all necessary is that if an Encyclopaedia is created in an init block,
        there's no way to save the data without using persistent data, but you don't want the init to reset
        the persistent data each time the game opens.
        """
        global persistent
        
        # Set the status variables to the dictionary values.
        master_key = master_key + "_0%s"
        vals_name = name + "_vals"
        dict_name = name + "_dict"

        try:
            # Set every value in persistent.<vals_name> to be a key in persistent.<dict_name> 
            dict_of_keys = self._make_persistent_dict(
                entries_total,
                master_key,
                'persistent.%s["%s"]' % (dict_name, master_key)
            )
            
            # Set persistent.<vals_name> to be a dictionary
            setattr(
                persistent,
                vals_name,
                dict_of_keys
            )
            
        except (TypeError, KeyError) as e:
            # The first time the Encyclopaedia is launched,
            # the persistent dictionary doesn't exist yet, causing a TypeError.
            # In development, the dictionary may already exist,
            # but without the correct number of keys, causing a KeyError.
            setattr(
                persistent,
                vals_name,
                {master_key % k: None for k in range(entries_total)}
            )
            
        # Set every value in persistent.new_dict to be a key in persistent.new_vals    
        dict_of_values = self._make_persistent_dict(
            entries_total,
            master_key,
            'persistent.%s["%s"]' % (vals_name, master_key))

        setattr(
            persistent,
            dict_name,
            dict_of_values
        )

    def addEntry(self, item):
        """Adds an entry to the encyclopaedia and sorts it."""
        
        # Add to list of all entries
        if not item in self.all_entries:  # Prevents duplicate entries
            self.all_entries.append(item)

        # Add to list of unlocked entries
        # The unlocked_entries list should only contain entries that have locked=False
        if not item in self.unlocked_entries:  # Prevents duplicate entries
            if item.locked is False:
                self.unlocked_entries.append(item)

        # Add the subject to the list
        self.addSubject(item.subject)
                
        self.sort_entries(
            sorting=self.sorting_mode,
            reverse=self.reverseSorting
        )

        self._size = len(self.unlocked_entries)
        self._size_all = len(self.all_entries)

    def addEntries(self, *new_entries): 
        """Adds multiple new entries at once"""
        for item in new_entries:
            self.addEntry(item)

    def addSubject(self, new_subject): 
        """
        Adds a new subject to the Encyclopaedia. Won't allow duplicates
        
        Returns:
            True if the subject was added, False if it was not
        """
        if not new_subject in self.subjects:
            self.subjects.append(new_subject)
            return True
        return False

    def addSubjects(self, *new_subjects): 
        """Adds multiple new subjects at once"""
        for item in new_subjects:
            self.addSubject(item)                
                
    def PreviousEntry(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangeEntryAction(self, -1, self.check_min(self.current_position, 0))

    def NextEntry(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangeEntryAction(self, 1, self.check_max(self.current_position, self.max_size - 1))

    def PreviousPage(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangePageAction(self, -2, -1, self.check_min(self.sub_current_position, 1))

    def NextPage(self):
        """
        Returns:
            Screen Action. Use with a button
        """
        return actions.ChangePageAction(self, 0, 1, self.check_max(self.sub_current_position, self.active.pages))

    def Sort(self, sorting_mode=None):
        """        
        Parameters: 
            sorting_mode: The type of sorting to use. If None specified, use the current sorting.
        
        Returns:
            Screen Action. Use with a button.
        """
        if None == sorting_mode:
            sorting_mode = self.sorting_mode
        return actions.SortEncyclopaedia(self, sorting_mode)

    def SetEntry(self,given_entry):
        """
        Returns:
            Screen Action. Use with a button.
        """
        return actions.SetEntryAction(self, given_entry)

    def SaveStatus(self, enc_dict, tag_string):
        """
        Returns:
            Screen Action. Use with a button.
        """
        return actions.SaveStatusAction(self, enc_dict, tag_string)

    def ChangeStatus(self, position):
        """
        Returns:
            Screen Action. Use with a button.
        """
        return actions.ChangeStatusAction(self, position)

    def ResetSubPage(self):
        """
        Returns:
            Screen Action. Use with a button.
        """
        return actions.ResetSubPageAction(self)

    def ToggleShowLockedButtons(self):
        """
        Returns:
            Screen Action. Use with a button.
        """
        return actions.ToggleShowLockedButtonsAction(self)

    def ToggleShowLockedEntry(self):
        """
        Returns:
            Screen Action. Use with a button.
        """
        return actions.ToggleShowLockedEntryAction(self)
