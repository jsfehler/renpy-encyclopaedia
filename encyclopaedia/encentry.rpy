init python:
    from operator import itemgetter

    from renpy.python import RevertableList


    class EncEntry(store.object):
        """Stores an Entry's content.
        EncEntry instances should be added to an Encyclopaedia.

        Args:
            parent (Encyclopaedia|EncEntry)
            number (int)
            name (str)
            text (str|list)
            subject (str)
            viewed (bool)
            locked (bool)
            image (str)
            locked_name (str)
            locked_text (str)
            locked_image (str)
            locked_image_tint (tuple)

        Attributes:
            has_image (bool): True if image was provided, else False.
            pages (int): Number of pages this entry contains.

            has_sub_entry (bool): If an entry has any sub-entries.
        """
        def __init__(self,
                     parent=None,
                     number=None,
                     name="",
                     text="",
                     subject="",
                     viewed=None,
                     viewed_persistent=None,
                     locked=False,
                     image=None,
                     locked_name="???",
                     locked_text="???",
                     locked_image=None,
                     locked_image_tint=(0.0, 0.0, 0.0)):

            self.number = number
            self._name = name
            self._text = self._string_to_list(text)
            self._viewed = viewed
            self.subject = subject
            self.locked = locked

            self.locked_name = locked_name
            self.locked_text = self._string_to_list(locked_text)
            self.locked_image = locked_image

            self.has_image = False
            if image is not None:
                self._image = image
                self.has_image = True

                # If there's an image, but no locked image is specified,
                # tint the image and use it as the locked image.
                if locked_image is None:
                    # Tuple is used to set the numbers that tint_locked_image()
                    # uses to change the colour of a locked image
                    self._tint_locked_image(locked_image_tint)

            self.pages = 0

            # List: The sub-entries and their position.
            #   The parent EncEntry must be the first in the sub-entry list.
            self.sub_entry_list = [[1, self]]

            self.has_sub_entry = False

            # Property: Set with Integer, get returns the page.
            self.current_page = 1

            # Place the entry into the assigned Encyclopaedia or EncEntry.
            if parent is not None:
                parent.add_entry(self)

            self.viewed_callback = None

            # When viewed is persistent, we get the viewed flag from persistent
            self.viewed_persistent = viewed_persistent
            if self.viewed_persistent:
                self._viewed = getattr(persistent, self.label + "_viewed")

        def __repr__(self):
            return "EncEntry: {}".format(self.label)

        @property
        def viewed(self):
            return self._viewed

        @viewed.setter
        def viewed(self, new_value):
            if self.viewed_persistent:
                setattr(persistent, self.label + "_viewed", new_value)

            self._viewed = new_value

        @property
        def label(self):
            """
            Returns:
                str: The number and name of the entry, in the format of:
                    "number: name"
            """
            return "{:02}: {}".format(self.number, self.name)

        @property
        def current_page(self):
            """
            Returns:
                EncEntry: The page of an entry that is currently being viewed.
            """
            return self._current_page

        @current_page.getter
        def current_page(self):
            return self.sub_entry_list[self._current_page][1]

        @current_page.setter
        def current_page(self, val):
            self._current_page = val - 1

        @staticmethod
        def _string_to_list(given_text):
            """Accepts a string or a list of strings for the 'given_text' argument.
            Each list item represents a paragraph.
            If a string is given, convert it to a list,
            assuming a string with no list = one paragraph.

            Args:
                given_text: The string or list of strings for the entry's text

            Returns:
                list
            """
            # If the text is already in a list, just return it.
            if type(given_text) is RevertableList:
                return given_text
            return [given_text]

        def __get_entry_data(self, data, locked_data):
            """Used by self.name, self.text, and self.image to control if
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
            """The name for the entry.
            If the entry is locked, returns the placeholder instead.

            Returns:
                str: The name for the EncEntry
            """
            return self._name

        @name.getter
        def name(self):
            return self.__get_entry_data(self._name, self.locked_name)

        @name.setter
        def name(self, val):
            self._name = val

            self.viewed = False

        @property
        def text(self):
            """The text for the entry.
            If the entry is locked, returns the placeholder instead.

            Returns:
                The text for the EncEntry
            """
            return self._text

        @text.getter
        def text(self):
            return self.__get_entry_data(self._text, self.locked_text)

        @text.setter
        def text(self, val):
            self._text = val

            self.viewed = False

        @property
        def image(self):
            """The image for the entry.
            If the entry is locked, returns the placeholder instead.

            Returns:
                The image for the EncEntry
            """
            return self._image

        @image.getter
        def image(self):
            return self.__get_entry_data(self._image, self.locked_image)

        @image.setter
        def image(self, val):
            self.has_image = True
            self._image = val

            self.viewed = False

        def _tint_locked_image(self, tint_amount):
            """If the EncEntry has an image but no locked image, tint the image
            and use it as the locked image.

            Args:
                tint_amount: Tuple for the RGB values to tint the image

            Returns:
                bool: True if successful, else False
            """
            if self.has_image:
                matrix = im.matrix.tint(
                    tint_amount[0],
                    tint_amount[1],
                    tint_amount[2]
                )
                self.locked_image = im.MatrixColor(
                    self._image,
                    matrix
                )
                return True

            return False

        def add_entry(self, sub_entry):
            """Adds multiple pages to the entry in the form of sub-entries.

            Args:
                sub_entry: The entry to add as a sub-entry.

            Returns:
                bool: True if anything was added, else False
            """
            if sub_entry.number is None:
                sub_entry.number = self.pages + 1

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

        def unlock_sub_entry(self, entry):
            """
            Changes the locked status of an entry,
            Then adds it as a sub-entry.

            Args:
                entry: The sub-entry to unlock
                unlock_flag: The flag to set the entry's locked status to
            """
            entry.locked = False

            self.add_entry(entry)

            self.viewed = False
