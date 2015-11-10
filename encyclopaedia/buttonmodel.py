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

import renpy.exports as renpy

ui = renpy.ui


def __unread_tag(encyclopaedia):
    """
    Default is an inactive textbutton.
    If you don't want that then override this function.

    Parameters:
        encyclopaedia: The encyclopaedia associated with the Entry.

    Returns:
        Ren'py displayable for indicating that an Entry is unread
    """
    tag = ui.textbutton(encyclopaedia.labels.unread_entry_label)
    return tag


def __entry_button(encyclopaedia, entry):
    """
    Default is a textbutton.
    If you don't want that then override this function.

    Returns:
        A button to open an Entry.
    """

    tag = ui.textbutton(
        entry.name,
        clicked=encyclopaedia.SetEntry(entry)
    )

    return tag


def __placeholder_entry_button(encyclopaedia, entry):
    """
    Default is a textbutton.
    If you don't want that then override this function.

    Returns:
        A placeholder button to open a locked Entry.
    """
    tag = ui.textbutton(
        encyclopaedia.labels.locked_entry_label,
        clicked=encyclopaedia.SetEntry(entry)
    )

    return tag


def __inactive_placeholder_entry_button(label):
    """
    Default is a textbutton.
    If you don't want that then override this function.

    Returns:
        An inactive placeholder for a locked Entry.
    """
    tag = ui.textbutton(label)
    return tag


def __add_entry_button(enc, position):
    """ 
    Add a single button for an Entry in an Encyclopaedia.

    Call this function on a Ren'Py screen, inside whatever other UI
    (Window, box, etc) you want, usually inside a for loop.

    Override this function if you want the buttons to display in a
    different way.

    Parameters:
        enc: The Encyclopaedia object to get data from

        position: the Entry's position in the Encyclopaedia's list of entries.
        It will reference either all the entries or only the unlocked ones,
        depending on the given Encyclopaedia's show_locked_buttons variable.
    """
    # If locked buttons should be visible.
    if enc.show_locked_buttons:

        entry = enc.all_entries[position]

        # If the entry is unlocked, add an active button.
        if entry.locked is False:
            __entry_button(enc, entry)

            # Add tag next to the button, if it hasn't been viewed yet.
            if not entry.status:
                __unread_tag(enc)

        # If the entry is locked, add an inactive button.
        else:
            # If locked entries should be visible, add an active button
            # with placeholder text.
            if enc.show_locked_entry:
                __placeholder_entry_button(enc, entry)
            else:
                __inactive_placeholder_entry_button(
                    enc.labels.locked_entry_label
                )

    # If locked buttons should not be visible.
    # ie: No need for placeholders.
    elif enc.show_locked_buttons is False:
        entry = enc.unlocked_entries[position]

        __entry_button(enc, entry)
        
        # Add tag next to the button, if it hasn't been viewed yet.
        if not entry.status:
            __unread_tag(enc)


def generate_entry_list_buttons(enc):
    """
    Depending on sorting mode, generates a button for each Encyclopaedia entry.

    Override this function if you want the buttons to display in a
    different way.

    Parameters:
        enc: The Encyclopaedia object to get data from
    """

    # If sorting by subject, display the subject heading and
    # add an entry under it if it's the same subject
    if enc.sorting_mode == enc.SORT_SUBJECT:
        for item in enc.subjects:
            ui.text(item)
            for y in range(enc.entry_list_size):
                if enc.get_entry_at(y).subject == item:
                    ui.hbox()
                    __add_entry_button(enc, y)
                    ui.close()

    # If sorting by number, add the number next to the entry
    elif enc.sorting_mode == enc.SORT_NUMBER:
        for x in range(enc.entry_list_size):
            ui.hbox()
            ui.textbutton(str(enc.get_entry_at(x).number))
            ui.hbox()
            __add_entry_button(enc, x)
            ui.close()
            ui.close()

    # If sorting Alphabetically or Reverse-Alphabetically,
    # don't add anything before the entry
    else:
        for x in range(enc.entry_list_size):
            ui.hbox()
            __add_entry_button(enc, x)
            ui.close()