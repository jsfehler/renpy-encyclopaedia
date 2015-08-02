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

from operator import itemgetter

import renpy.store as store
import renpy.exports as renpy


class EncEntry(store.object):
    """Stores an Entry's content. EncEntry should be added to an Encyclopaedia."""
    def __init__(self, number=0, name="Entry Name", text="Entry Text", subject=None, status=None, locked=False, image=None, locked_name="???", locked_text="???", locked_image=None):  
        self.number = number
        self.name = name
        self.text = self._string_to_list(text)
        self.status = status
        self.subject = subject
        self.locked = locked
        
        # Only set the image if it's not None
        self.has_image = False  
        if image != None:
            self.image = image

            # If there's an image, but no locked image is specified, tint the image and use it as the locked image.
            if locked_image == None:
                 # Tuple is used to set the numbers that tint_locked_image() uses to change the colour of a locked image
                self.tint_locked_image((0.0, 0.0, 0.0))
            
        self.locked_name = locked_name
        self.locked_text = self._string_to_list(locked_text)
        self.locked_image = locked_image

        # Number of pages in the entry
        self.pages = 0

        # The parent EncEntry must be the first entry in the sub-entry list.
        self.sub_entry_list = [[1, self]]
        
        # Default status for an Entry is to have no sub-entries
        self.has_sub_entry = False
        
        self.current_page = 1

    @property
    def current_page(self):
        return self._current_page

    @current_page.getter
    def current_page(self):
        return self.sub_entry_list[self._current_page][1]
        
    @current_page.setter
    def current_page(self, val):
        self._current_page = val -1
        
    def _string_to_list(self, given_text):
        """
        EncEntry accepts a string or a list of strings for the 'text' argument.
        Each list item is a paragraph.
        If a string is given, convert it to a list.
        """
        # If the text is already in a list, just return it.
        if type(given_text) is renpy.python.RevertableList:
            return given_text
        return [given_text]        
        
    def __repr__(self):
        return "EncEntry: " + str(self.name) 

    def __str__(self):
        return str(self.name)

    def _get_entry_data(self, data, locked_data):
        """
        Used by self.name, self.text, and self.image to control if the locked placeholder or actual entry data should be returned.
        
        Returns:
            If True or None, return the data requested, else return the locked placeholder for the data
        """
        if self.locked or self.locked == None:
            return locked_data
        return data

    @property
    def name(self):
        """
        The name for the entry. If the entry is locked, returns the placeholder instead
        
        Returns:
            The name for the EncEntry
        
        """
        return self._name
        
    @name.getter
    def name(self):
        return self._get_entry_data(self._name, self.locked_name)
        
    @name.setter
    def name(self, val):
        self._name = val
        
    @property
    def text(self):
        """
        The text for the entry. If the entry is locked, returns the placeholder instead
        
        Returns:
            The text for the EncEntry
        """
        return self._text
        
    @text.getter
    def text(self):
        return self._get_entry_data(self._text, self.locked_text)
        
    @text.setter
    def text(self, val):
        self._text = val      

    @property
    def image(self):
        """
        The image for the entry. If the entry is locked, returns the placeholder instead
        
        Returns:
            The image for the EncEntry
        """
        return self._image
        
    @image.getter
    def image(self):
        return self._get_entry_data(self._image, self.locked_image)

    @image.setter
    def image(self, val):
        self.has_image = True
        self._image = val   

    def tint_locked_image(self, tint_amount):
        """
        If the EncEntry has an image, tint it and use it as the locked image.
        
        Parameters:
            tint_amount: Tuple for the RGB values to tint the image
        
        Returns:
            True if successful. Exception if not
        """
        if self.has_image:
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