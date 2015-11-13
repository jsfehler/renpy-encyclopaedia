from operator import itemgetter

import renpy.store as store
import renpy.exports as renpy

from encexceptions import MissingImageError


class EncEntry(store.object):
    """
    Stores an Entry's content.
    EncEntry should be added to an Encyclopaedia.
    """
    def __init__(self,
                 number=0,
                 name="Entry Name",
                 text="Entry Text",
                 subject=None,
                 status=None,
                 locked=False,
                 image=None,
                 locked_name="???",
                 locked_text="???",
                 locked_image=None):
        self.number = number
        self.name = name
        self.text = self._string_to_list(text)
        self.status = status
        self.subject = subject
        self.locked = locked
        
        self.locked_name = locked_name
        self.locked_text = self._string_to_list(locked_text)
        self.locked_image = locked_image

        # Boolean: If the Entry has an image. Set in the image property.
        self.has_image = False  
        if image is not None:
            self.image = image

            # If there's an image, but no locked image is specified,
            # tint the image and use it as the locked image.
            if locked_image is None:
                # Tuple is used to set the numbers that tint_locked_image()
                # uses to change the colour of a locked image
                self.tint_locked_image((0.0, 0.0, 0.0))
            
        # Integer: Number of pages in the entry
        self.pages = 0

        # List: The sub-entries and their position.
        #   The parent EncEntry must be the one in the sub-entry list.
        self.sub_entry_list = [[1, self]]
        
        # Boolean: If an entry has any sub-entries
        self.has_sub_entry = False

        # Property: Set with Integer, get returns the page.
        self.current_page = 1

    @property
    def current_page(self):
        """
        Returns:
            EncEntry: The page of an entry that is currently being viewed.
        """
        return self._current_page

    @current_page.getter
    def current_page(self):
        """
        Getter for current_page property.
        """
        return self.sub_entry_list[self._current_page][1]
        
    @current_page.setter
    def current_page(self, val):
        """
        Setter for current_page property.
        """
        self._current_page = val - 1

    @staticmethod
    def _string_to_list(given_text):
        """
        EncEntry accepts a string or a list of strings for the 'text' argument.
        Each list item represents a paragraph.
        If a string is given, convert it to a list,
        assuming a string with no list = one paragraph.

        Parameters:
            given_text: The string or list of strings for the entry's text

        Returns:
            list
        """
        # If the text is already in a list, just return it.
        if type(given_text) is renpy.python.RevertableList:
            return given_text
        return [given_text]        
        
    def __repr__(self):
        return "EncEntry: " + str(self.name) 

    def __str__(self):
        return str(self.name)

    def __get_entry_data(self, data, locked_data):
        """
        Used by self.name, self.text, and self.image to control if
        the locked placeholder or actual entry data should be returned.
        
        Returns:
            If True or None, return the data requested,
            otherwise the placeholder for the data
        """
        if self.locked or self.locked is None:
            return locked_data
        return data

    @property
    def name(self):
        """
        The name for the entry.
        If the entry is locked, returns the placeholder instead.
        
        Returns:
            str: The name for the EncEntry
        """
        return self._name
        
    @name.getter
    def name(self):
        """
        Getter for name property.
        """
        return self.__get_entry_data(self._name, self.locked_name)
        
    @name.setter
    def name(self, val):
        """
        Setter for name property.
        """
        self._name = val
        
    @property
    def text(self):
        """
        The text for the entry.
        If the entry is locked, returns the placeholder instead.
        
        Returns:
            The text for the EncEntry
        """
        return self._text
        
    @text.getter
    def text(self):
        """
        Getter for text property.
        """
        return self.__get_entry_data(self._text, self.locked_text)
        
    @text.setter
    def text(self, val):
        """
        Setter for text property.
        """
        self._text = val

    @property
    def image(self):
        """
        The image for the entry.
        If the entry is locked, returns the placeholder instead.
        
        Returns:
            The image for the EncEntry
        """
        return self._image
        
    @image.getter
    def image(self):
        """
        Getter for image property.
        """
        return self.__get_entry_data(self._image, self.locked_image)

    @image.setter
    def image(self, val):
        """
        Setter for image property.
        """
        self.has_image = True
        self._image = val   

    def tint_locked_image(self, tint_amount):
        """
        If the EncEntry has an image but no locked image,
        tint the image and use it as the locked image.

        Parameters:
            tint_amount: Tuple for the RGB values to tint the image
        
        Returns:
            bool: True if successful

        Raises:
            MissingImageError: If you try to tint an entry with no image
        """
        if self.has_image:
            matrix = renpy.display.im.matrix.tint(
                tint_amount[0],
                tint_amount[1],
                tint_amount[2]
            )
            self.locked_image = renpy.display.im.MatrixColor(
                self._image,
                matrix
            )
            return True

        raise MissingImageError(
            "EncEntry has no image. Cannot tint nothing."
        )

    def add_sub_entry(self, sub_entry):
        """
        Adds multiple pages to the entry in the form of sub-entries.

        Parameters:
            sub_entry: The entry to add as a sub-entry.

        Returns:
            True if successful
        """
        if not [sub_entry.number, sub_entry] in self.sub_entry_list:
            if sub_entry.locked is False:
                self.sub_entry_list.append([sub_entry.number, sub_entry])
                self.sub_entry_list = sorted(
                    self.sub_entry_list,
                    key=itemgetter(0)
                )
                self.has_sub_entry = True

                self.pages = len(self.sub_entry_list)
                return True
        return False

    def add_sub_entries(self, *new_sub_entries):
        """
        Adds multiple new sub-entries at once.
        """
        for item in new_sub_entries:
            self.add_sub_entry(item)

    def unlock_sub_entry(self, entry, unlock_flag):
        """
        Changes the locked status of an entry,
        Then adds it as a sub-entry.

        Parameters:
            entry: The sub-entry to unlock
            unlock_flag: The flag to set the entry's locked status to
        """
        entry.locked = unlock_flag

        self.add_sub_entry(entry)
        
        # If an entry gets sub-entries unlocked,
        # the unread status on the entire entry is restored
        self.status = False
