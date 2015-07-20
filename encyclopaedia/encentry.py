from operator import itemgetter

import renpy.store as store
import renpy.exports as renpy


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

        self.has_image = False  
        if image != None: # If no image, assume the entry was meant to have no image
            self.image = image
            self.has_image = True

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