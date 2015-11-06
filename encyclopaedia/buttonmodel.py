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


def generate_entry_button(position, enc):
    """ 
    Create a single button for an Entry in an Encyclopaedia.
    Call this function on a Ren'Py screen, inside whatever other UI
    (Window, box, etc) you want, inside a for loop.

    Override this function if you want the buttons to display in a
    different way.

    Parameters:
        position: the Entry's position in the Encyclopaedia's list of entries.
        It will reference either all the entries or only the unlocked ones,
        depending on the given Encyclopaedia's show_locked_buttons variable.
    
        enc: The given Encyclopaedia.
    """
    # If locked buttons should be visible.
    if enc.show_locked_buttons:
        # If the entry is unlocked, make the button point to it.
        # If it's locked, make a "???" button.
        if enc.all_entries[position].locked is False:
            ui.textbutton(
                enc.all_entries[position].name,
                clicked=enc.SetEntry(enc.all_entries[position])
            )
            
            # Make a tag next to the button,
            # if it hasn't been viewed by the player yet.
            if not enc.all_entries[position].status:
                ui.textbutton(enc.labels.unread_entry_label)

        else:
            # If locked entries should be viewable,
            # the "???" button should go to the entry.
            # If not, it's an inactive button.
            if enc.show_locked_entry:
                ui.textbutton(
                    enc.labels.locked_entry_label,
                    clicked=enc.SetEntry(enc.all_entries[position])
                )
            else:
                ui.textbutton(enc.labels.locked_entry_label)

    # If locked buttons should not be visible. (No need for the "???" buttons.)
    elif enc.show_locked_buttons is False:
        ui.textbutton(
            enc.unlocked_entries[position].name,
            clicked=enc.SetEntry(enc.unlocked_entries[position]))
        
        # Make a tag next to the button
        # if it hasn't been viewed by the player yet.
        if not enc.unlocked_entries[position].status:
            ui.textbutton(enc.labels.unread_entry_label)


def generate_entry_list_buttons(enc):
    """
    Generates a button for each Encyclopaedia entry.

    Override this function if you want the buttons to display in a
    different way.

    Parameters:
        enc: The Encyclopaedia object to get data from
    """

    # If sorting by subject, display the subject heading and
    # add an entry under it if it's the same subject
    if enc.sorting_mode == enc.SORT_SUBJECT:

        for number, item in enumerate(enc.subjects):
            ui.text(item)
            for y in range(enc.entry_list_size):
                if enc.get_entry_at(y).subject == item:
                    ui.hbox()
                    generate_entry_button(y, enc)
                    ui.close()

    # If sorting by number, add the number next to the entry
    elif enc.sorting_mode == enc.SORT_NUMBER:
        for x in range(enc.entry_list_size):
            ui.hbox()
            ui.textbutton(str(enc.get_entry_at(x).number))
            ui.hbox()
            generate_entry_button(x, enc)
            ui.close()
            ui.close()

    # If sorting Alphabetically or Reverse-Alphabetically,
    # don't add anything before the entry
    else:
        for x in range(enc.entry_list_size):
            ui.hbox()
            generate_entry_button(x, enc)
            ui.close()