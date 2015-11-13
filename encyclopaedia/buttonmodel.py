from itertools import groupby

import renpy.exports as renpy

ui = renpy.ui


class ButtonModel(object):
    """
    Subclass this to override and use custom ways of displaying buttons.
    """
    def __init__(self, encyclopaedia):
        self.enc = encyclopaedia

    def __unread_tag(self):
        """
        Default is an inactive textbutton.
        If you don't want that then override this function.

        Parameters:
            encyclopaedia: The encyclopaedia associated with the Entry.

        Returns:
            Ren'py displayable for indicating that an Entry is unread
        """
        tag = ui.textbutton(self.enc.labels.unread_entry_label)
        return tag

    def __entry_button(self, entry):
        """
        Default is a textbutton.
        If you don't want that then override this function.

        Returns:
            A button to open an Entry.
        """
        tag = ui.textbutton(
            entry.name,
            clicked=self.enc.SetEntry(entry)
        )

        return tag

    def __placeholder_entry_button(self, entry):
        """
        Default is a textbutton.
        If you don't want that then override this function.

        Returns:
            A placeholder button to open a locked Entry.
        """
        tag = ui.textbutton(
            self.enc.labels.locked_entry_label,
            clicked=self.enc.SetEntry(entry)
        )

        return tag

    def __inactive_placeholder_entry_button(self):
        """
        Default is a textbutton.
        If you don't want that then override this function.

        Returns:
            An inactive placeholder for a locked Entry.
        """
        tag = ui.textbutton(self.enc.labels.locked_entry_label)
        return tag

    def __add_entry_button(self, entry):
        """
        Add a single button for an Entry in an Encyclopaedia.

        Call this function on a Ren'Py screen, inside whatever other UI
        (Window, box, etc) you want, usually inside a for loop.

        Override this function if you want the buttons to display in a
        different way.

        Parameters:
            enc: The Encyclopaedia object to get data from

            position: the Entry's position in the Encyclopaedia's list of
                entries. It will reference either all the entries or
                only the unlocked ones, depending on
                the given Encyclopaedia's show_locked_buttons variable.
        """
        # If locked buttons should be visible.
        if self.enc.show_locked_buttons:

            # If the entry is unlocked, add an active button.
            if entry.locked is False:
                self.__entry_button(entry)

                # Add tag next to the button, if it hasn't been viewed yet.
                if not entry.status:
                    self.__unread_tag()

            # If the entry is locked, add an inactive button.
            else:
                # If locked entries should be visible, add an active button
                # with placeholder text.
                if self.enc.show_locked_entry:
                    self.__placeholder_entry_button(entry)
                else:
                    self.__inactive_placeholder_entry_button()

        # If locked buttons should not be visible.
        # ie: No need for placeholders.
        elif self.enc.show_locked_buttons is False:
            self.__entry_button(entry)

            # Add tag next to the button, if it hasn't been viewed yet.
            if not entry.status:
                self.__unread_tag()

    def display_vertical_list(self):
        """
        Depending on sorting mode, generates a button for each
        Encyclopaedia entry and displays them vertically.

        Parameters:
            enc: The Encyclopaedia object to get data from
        """
        # The list is chosen based on if we want to show locked entries on
        # the entry select screen or not.
        if self.enc.show_locked_buttons:
            entries = self.enc.all_entries
        else:
            entries = self.enc.unlocked_entries

        # If sorting by subject, display the subject heading and
        # add an entry under it if it's the same subject
        if self.enc.sorting_mode == self.enc.SORT_SUBJECT:
            # Split entries by subject
            for key, group in groupby(entries, lambda x: x.subject):
                ui.text(key)
                for entry in group:
                    ui.hbox()
                    self.__add_entry_button(entry)
                    ui.close()

        # If sorting by number, add the number next to the entry
        elif self.enc.sorting_mode == self.enc.SORT_NUMBER:
            for entry in entries:
                ui.hbox()
                ui.textbutton(str(entry.number))
                ui.hbox()
                self.__add_entry_button(entry)
                ui.close()
                ui.close()

        # If sorting Alphabetically, Reverse-Alphabetically, or Unread.
        else:
            if self.enc.nest_alphabetical_sort:
                for key, group in groupby(entries, lambda x: x.name[0]):
                    ui.text(key)
                    for entry in group:
                        ui.hbox()
                        self.__add_entry_button(entry)
                        ui.close()

            else:
                for entry in entries:
                    ui.hbox()
                    self.__add_entry_button(entry)
                    ui.close()