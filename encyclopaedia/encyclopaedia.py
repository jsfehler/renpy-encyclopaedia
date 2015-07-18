# Encyclopaedia Framework 2.0 for Ren'Py
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
from operator import itemgetter

import renpy.store as store
import renpy.exports as renpy 

from entrylist import EntryList

persistent = renpy.game.persistent


class EncyclopaediaEntryAction(renpy.ui.Action):
    """Action that acts using a specific Encyclopaedia Entry"""
    def __init__(self, encyclopaedia, entry_number):
        self.enc = encyclopaedia
        self.entry_number = entry_number    

    def _string_to_list(self, given_text):
        """
        The text for an Encyclopaedia Entry can be a string or a list of strings.
        If a string is given, convert it to a list.
        """
        # If the text is already in a list, just return it.
        if type(given_text) is renpy.python.RevertableList:
            return given_text
        return [given_text]


class SetEntryAction(EncyclopaediaEntryAction):
    """Action that sets the selected encyclopaedia entry into the displaying frame."""       
            
    def __call__(self):
        self.given_entry = self.enc.get_entry_at(self.entry_number)
        self.given_text = self.given_entry.text
        
        # entry_text is the variable used on the encyclopaedia_entry screen for whatever entry's text we're displaying            
        self.enc.entry_text = self._string_to_list(self.given_text)

        # index the list to get what the new current_position should be
        if self.enc.showLockedEntry:
            target_position = self.enc.all_entries.index([self.given_entry.number, self.given_entry])
        else:
            target_position = self.enc.unlocked_entries.index([self.given_entry.number, self.given_entry])

        # The EntryData is based on the target_position gotten
        self.enc.index = target_position

        self.enc.current_position = target_position


class ChangeEntryAction(EncyclopaediaEntryAction):
    """  
    Scroll through the current entry being viewed. 
    Used by an Encyclopaedia's PreviousEntry and NextEntry functions.
    """    
    def __init__(self, encyclopaedia, direction, block, *args, **kwargs):  
        self.enc = encyclopaedia
        self.block = block # If the button is active or not
        self.dir = direction  # Determines if it's going to the previous or next entry 

    def __call__(self):
        if self.block == False:
            new_position = self.enc.current_position + self.dir
            
            self.enc.index = new_position

            entries = self.enc.all_entries
            if self.enc.showLockedEntry == False:
                entries = self.enc.unlocked_entries

            entries[new_position][1].status = True 
            given_text = entries[new_position][1].text   
          
            self.enc.entry_text = self._string_to_list(given_text)

            self.enc.current_position += self.dir
  
            # When changing an entry, the sub-entry page number is set back to 1
            self.enc.sub_current_position = 1
            renpy.restart_interaction()

    def get_sensitive(self):
        if self.block:
            return False
        return True 


class ChangePageAction(ChangeEntryAction):
    """Change the current sub-entry being viewed."""        
    def __init__(self, encyclopaedia, direction, direction2, block, *args, **kwargs):
        super(ChangePageAction,self).__init__(encyclopaedia, direction, block, *args, **kwargs)

        self.dir1 = direction
        self.dir2 = direction2

    def __call__(self):
        if self.block == False: 
            given_text = self.enc.get_unlocked_entry_at(self.enc.current_position).getSubEntry(self.enc.sub_current_position + self.dir1)

            self.enc.entry_text = self._string_to_list(given_text)
            
            self.enc.sub_current_position += self.dir2

            renpy.restart_interaction()


class SortEncyclopaedia(renpy.ui.Action):
    """Sorts the entries based on sorting_mode"""        
    def __init__(self, encyclopaedia, sorting_mode=0):
        self.enc = encyclopaedia
        self.sorting_mode = sorting_mode
        
        self.reverse = False
        if sorting_mode == self.enc.SORT_REVERSE_ALPHABETICALLY:
            self.reverse = True
        
    def __call__(self):
        self.enc.sort_entries(sorting=self.sorting_mode, reverse=self.reverse)

        self.enc.sorting_mode = self.sorting_mode
        renpy.restart_interaction()


class SaveStatusAction(renpy.ui.Action):
    """
    Saves the "New!" status of every entry in an encyclopaedia. 
    Only necessary if using Persistent Data.
    """
    def __init__(self, encyclopaedia, enc_dict, tag_string):
        self.enc = encyclopaedia
        self.enc_dict = enc_dict
        self.tag_string = tag_string
    
    def __call__(self):
        for x in range(self.enc.size_all):
            self.enc_dict[self.tag_string + str(x)] = self.enc.all_entries[x][1].status   


class ChangeStatusAction(EncyclopaediaEntryAction): 
    """Change the "New!" status of an EncEntry"""    
    def __call__(self):
        self.changed_entry = self.enc.get_entry_at(self.entry_number)
        self.changed_entry.status = True


class ResetSubPageAction(renpy.ui.Action):
    """Resets the sub-page count to 1. Used when closing the entry screen."""    
    def __init__(self, encyclopaedia):
        self.enc = encyclopaedia   
    
    def __call__(self):
        self.enc.sub_current_position = 1
        renpy.restart_interaction()

        
class ToggleShowLockedButtonsAction(renpy.ui.Action):
    """
    Toggles if locked Entries will be shown in the list of Entries or not.
    For the sake of User Experience, this is best left as a debug option.
    """    
    def __init__(self, encyclopaedia):
        self.enc = encyclopaedia 

    def __call__(self):
        self.enc.showLockedButtons = not self.enc.showLockedButtons
        renpy.restart_interaction()


class ToggleShowLockedEntryAction(renpy.ui.Action):
    """
    Toggles if locked Entries can be viewed or not.
    For the sake of User Experience, this is best left as a debug option.
    """    
    def __init__(self, encyclopaedia):
        self.enc = encyclopaedia   
    
    def __call__(self):
        self.enc.showLockedEntry = not self.enc.showLockedEntry
        renpy.restart_interaction()
        
class Encyclopaedia(store.object): 
    """Container that manages the display and sorting of a group of EncEntries."""
    
    # Constants for the different types of sorting available.
    SORT_NUMBER = 0
    SORT_ALPHABETICALLY = 1
    SORT_REVERSE_ALPHABETICALLY = 2
    SORT_SUBJECT = 3
    SORT_UNREAD = 4
            
    def __init__(self, sorting_mode=0, showLockedButtons=False, showLockedEntry=False):
        self.subjects = [] # List of all subjects
        
        # List of unlocked entries
        self.unlocked_entries = EntryList()
        
        # List of all entries, regardless of if locked or not
        self.all_entries = EntryList() 
        
        self.size = 0  # length of self.unlocked_entries  
        self.size_all = 0 # length of self.all_entries  
        
        # The type of sorting used. Default sorting is by Number.
        self.sorting_mode = sorting_mode

        self.reverseSorting = False
        if sorting_mode == self.SORT_REVERSE_ALPHABETICALLY:
            self.reverseSorting = True

        # If True, locked entries show "???" on the listing screen.
        self.showLockedButtons = showLockedButtons 
        
        # If True, locked entries can be viewed, but the data is hidden from view
        self.showLockedEntry = showLockedEntry

        self.current_position = 0 # Indicates the current entry open. Is the current position based on the unlocked list.
        self.sub_current_position = 1 # 1 because the main entry is the first page in the sub-entry list

        self.index = 0

        self.entry_text = ""
        
        # Variables for the string representations of the different sorting types
        self.sort_number_label = "Number"
        self.sort_alphabetically_label = "A to Z"
        self.sort_reverse_alphabetically_label = "Z to A"
        self.sort_subject_label = "Subject"
        self.sort_unread_label = "Unread"        

    @property
    def index(self):
        return self._index
    
    @index.getter
    def index(self):
        """
        Returns:
            The entry at the index number.
        """
        return self.get_entry_at(self._index)

    @index.setter
    def index(self, val):
        self._index = val
        
    @property
    def entry_list_size(self):
        """
        Returns:
            Whatever the size of the entry list should be, based on if locked buttons should be shown or not.
        """
        if self.showLockedButtons:
            return self.size_all
        return self.size            

    @property
    def max_size(self):
        """
        Returns:
            Whatever the maximum size of the entry list should be, based on if locked buttons should be shown or not.
        """
        if self.showLockedEntry:
            return self.size_all
        return self.size
            
    @property
    def sorting_mode_label(self):
        """
        Returns:
            String representation the current sorting mode
        """
        sorting_strings = {self.SORT_NUMBER: self.sort_number_label,
        self.SORT_ALPHABETICALLY: self.sort_alphabetically_label,
        self.SORT_REVERSE_ALPHABETICALLY: self.sort_reverse_alphabetically_label,
        self.SORT_SUBJECT: self.sort_subject_label,
        self.SORT_UNREAD: self.sort_unread_label}

        return sorting_strings[self.sorting_mode]

    def get_percentage_unlocked_label(self, indicator='%'): 
        """
        Parameters:
            indicator: A string that is placed next to the percentage unlocked number
        
        Returns: 
            String representation of the percentage of the encyclopaedia that's unlocked, ie: '50%'
        """
        amount_unlocked = float(self.size) / float(self.size_all)
        percentage = floor(amount_unlocked * 100)
        return str(int(percentage)) + indicator

    def get_entry_current_page_label(self, label='Page', separator='/'):
        """
        Parameters:
            label: String placed before the entry page displayed
            separator: String placed in-between the current page number and the total page number 
        
        Returns: 
            String indicating which sub-page of an entry is being viewed
        """
        return "%s %d %s %d" % (label, self.sub_current_position, separator, self.index.pages)        
        
    def set_global_locked_image_tint(self, tint_amount):
        """Sets all the locked images in an Encyclopaedia to use the same tint.
        
        Parameters:
            tint_amount - tuple containing an RGB value (R, G, B)
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
        Sort both entry lists by whatever the current sorting mode is
        """
        # Sort lists so that the newly unlocked entries don't end up at the bottom of the list
        if sorting == self.SORT_NUMBER:
            self.all_entries._sort_by_number()
            self.unlocked_entries._sort_by_number()
        elif sorting == self.SORT_UNREAD:
            self.all_entries._sort_by_unread()
            self.unlocked_entries._sort_by_unread()
        else:
            self.all_entries._sort_by_name(reverse=reverse)
            self.unlocked_entries._sort_by_name(reverse=reverse)
        
    def addEntry(self, item): 
        """Adds an entry to the encyclopaedia and sorts it."""
        
        # Add to list of all entries
        if not [item.number, item] in self.all_entries: # Prevents duplicate entries
            self.all_entries.append([item.number, item])

        # Add to list of unlocked entries
        # The unlocked_entries list should only contain entries that have locked=False
        if not [item.number, item] in self.unlocked_entries: # Prevents duplicate entries
            if item.locked == False:
                self.unlocked_entries.append([item.number, item])

        self.sort_entries(sorting=self.sorting_mode, reverse=self.reverseSorting)

        self.size = len(self.unlocked_entries)
        self.size_all = len(self.all_entries)

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
      
    def get_entry_at(self, entry_number): 
        """ 
        Get the entry at a specific index.
        Used for displaying the buttons.
        Depends on if locked entries should be in the entry list or not.
        
        Returns: 
            The entry of the specified entry_number
        """
        if self.showLockedButtons:
            return self.get_all_entry_at(entry_number)
        return self.get_unlocked_entry_at(entry_number)

    def get_all_entry_at(self, entry_number): 
        """
        Returns: 
            The entry associated with entry_number from all_entries list
        """
        return self.all_entries[entry_number][1]

    def get_unlocked_entry_at(self, entry_number): 
        """
        Returns:
            The entry associated with entry_number from unlocked_entries list
        """
        return self.unlocked_entries[entry_number][1]
        
    # Checks the current_position against the min or max of the encyclopaedia, returns Boolean
    # Used to determine if the Prev/Next Actions should be active
    def checkMin(self, check_position, min):
        if check_position <= min:
            return True
        return False

    def checkMax(self, check_position, max):
        if check_position >= max:
            return True
        return False
 
    def _make_persistent_dict(self, total, dk, dv):
        """
        For the total amount given,
        takes a two strings to define a series of keys and values. 
        Creates lists and evaluates the values to variables. 
        Combines the lists into a dictionary.
        """
        keys = [dk % x for x in range(total)] # eg: new_00, new_01, etc
        vals_string = [dv % x for x in range(total)] # eg: persistent.new_dict["new_00"], persistent.new_dict["new_01"], etc
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
            # Set every value in persistent.new_vals to be a key in persistent.new_dict 
            dict_of_keys = self._make_persistent_dict(entries_total, master_key, 'persistent.%s["%s"]' % (dict_name, master_key))
            setattr(persistent, vals_name, dict_of_keys)
            
        except (TypeError, KeyError) as e:
            # The first time the Encyclopaedia is launched, the persistent dictionary doesn't exist yet, causing a TypeError. 
            # In development, the dictionary may already exist, but without the correct number of keys, causing a KeyError. 
            setattr(persistent, vals_name, {master_key % k: None for k in range(entries_total)})
            
        # Set every value in persistent.new_dict to be a key in persistent.new_vals    
        dict_of_values = self._make_persistent_dict(entries_total, master_key, 'persistent.%s["%s"]' % (vals_name, master_key))
        setattr(persistent, dict_name, dict_of_values)   

    # The following functions all bind Screen Actions to the Encyclopaedia Object.
    def PreviousEntry(self):
        return ChangeEntryAction(self, -1, self.checkMin(self.current_position, 0))

    def NextEntry(self):
        return ChangeEntryAction(self, 1, self.checkMax(self.current_position, self.max_size - 1))

    def PreviousPage(self):
        return ChangePageAction(self, -2, -1, self.checkMin(self.sub_current_position, 1))

    def NextPage(self):
        return ChangePageAction(self, 0, 1, self.checkMax(self.sub_current_position, self.index.pages))

    def Sort(self, sorting_mode=None):
        """
        Parameters: 
            sorting_mode: The type of sorting to use. If None, use the current sorting.
        """
        if None == sorting_mode:
            sorting_mode = self.sorting_mode
        return SortEncyclopaedia(self, sorting_mode)

    def SetEntry(self,given_entry):
        return SetEntryAction(self, given_entry) 

    def SaveStatus(self, enc_dict, tag_string):
        return SaveStatusAction(self, enc_dict, tag_string)

    def ChangeStatus(self, position):
        return ChangeStatusAction(self, position)

    def ResetSubPage(self):
        return ResetSubPageAction(self)

    def ToggleShowLockedButtons(self):
        return ToggleShowLockedButtonsAction(self) 

    def ToggleShowLockedEntry(self):
        return ToggleShowLockedEntryAction(self)  
        
        
class EncEntry(store.object):
    """Stores Entry content. Has to be added to an Encyclopaedia or else it will do nothing."""
    def __init__(self, number=0, name="Entry Name", text="Entry Text", subject=None, status=None, locked=False, image=None, locked_image=None):  
        self.number = number
        self.name = name
        self.text = text
        self.status = status
        self.subject = subject
        self.locked = locked
        self.locked_name = "???"
        self.locked_text = "???"
        self.locked_image = locked_image
        
        # Tuple used to set the numbers that tintLockedImage() uses to change the colour of a locked image
        self.locked_image_tint = (0.0, 0.0, 0.0) 

        # Number of pages in the entry
        self.pages = 0

        self.hasImage = False  
        if image != None: # If no image, assume the entry was meant to have no image
            self.image = image
            self.hasImage = True

            # If no locked image is specified, tint the entry image.
            if self.locked_image == None:
                self.tint_locked_image(self.locked_image_tint)

        self.sub_entry_list = [[1, self]]
        
        # Default status for an Entry is to have no sub-entries
        self.has_sub_entry = False

    def __repr__(self):
        return "EncEntry: " + str(self.name) 

    def __str__(self):
        return str(self.name)

    def _get_entry_data(self, data, locked_data):
        """
        Returns:
            If True or None, return the data requested, else the locked placeholder for the data
        """
        if self.locked or self.locked == None:
            return locked_data
        return data

    @property
    def name(self):
        """The name for the entry. If the entry is locked, returns the placeholder instead"""
        return self._name
        
    @name.getter
    def name(self):
        return self._get_entry_data(self._name, self.locked_name)
        
    @name.setter
    def name(self, val):
        self._name = val
        
    @property
    def text(self):
        """The text for the entry. If the entry is locked, returns the placeholder instead"""
        return self._text
        
    @text.getter
    def text(self):
        return self._get_entry_data(self._text, self.locked_text)
        
    @text.setter
    def text(self, val):
        self._text = val      

    @property
    def image(self):
        """The image for the entry. If the entry is locked, returns the placeholder instead"""
        return self._image
        
    @image.getter
    def image(self):
        return self._get_entry_data(self._image, self.locked_image)
        
    @image.setter
    def image(self, val):
        self._image = val   

    def tint_locked_image(self, tint_amount):
        if self.hasImage:
            matrix = renpy.display.im.matrix.tint(tint_amount[0], tint_amount[1], tint_amount[2] )
            self.locked_image = renpy.display.im.MatrixColor(self._image, matrix)
            return True
        raise Exception("EncEntry has no image. Cannot tint nothing.")

    def addSubEntry(self, sub_entry):
        """Adds multiple pages to the entry in the form of sub-entries."""
        if not [sub_entry.number, sub_entry] in self.sub_entry_list:
            if not sub_entry in self.sub_entry_list:
                if sub_entry.locked == False:
                    self.sub_entry_list.append([sub_entry.number, sub_entry])
                    self.sub_entry_list = sorted(self.sub_entry_list, key=itemgetter(0))
                    self.has_sub_entry = True
            
                    self.pages = len(self.sub_entry_list)
                    return True
        return False

    def addSubEntries(self, *new_sub_entries):
        """Adds multiple new sub-entries at once."""
        for item in new_sub_entries:
            self.addSubEntry(item)

    def getSubEntry(self, page):
        """Returns the text on given page."""
        return self.sub_entry_list[page][1].text

    def unlockSubEntry(self, item, unlock_flag):
        item.locked = unlock_flag
        self.addSubEntry(item)
        
        # If an entry gets sub-entries unlocked, the unread status on the entry is restored
        self.status = False