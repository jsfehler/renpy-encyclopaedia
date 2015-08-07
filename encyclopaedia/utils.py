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

def generate_entry_button(x, enc):
    """ 
    Create a single button for an Entry in an Encyclopaedia.
    Call this function on a Ren'Py screen, inside whatever other UI (Window, box, etc) you want, inside a for loop.
    
    Parameters:
        x: is the Entry's position in the Encyclopaedia's list of entries.
        It will reference either all the entries or only the unlocked ones, depending on the given Encyclopaedia's showLockedButtons variable.
    
        enc: The given Encyclopaedia.
    """
    ui.hbox()
    # If locked buttons should be visible.
    if enc.showLockedButtons:
        # If the entry is unlocked, make the button point to it. If it's locked, make a "???" button.
        if enc.all_entries[x].locked == False:
            ui.textbutton(enc.all_entries[x].name, clicked=enc.SetEntry(enc.all_entries[x]))
            
            # Make a tag next to the button if it hasn't been viewed by the player yet.
            if not enc.all_entries[x].status:    
                ui.textbutton ("New!")

        else:
            # If locked entries should be viewable, the "???" button should go to the entry. 
            # If not, it's an inactive button.
            if enc.showLockedEntry:
                ui.textbutton("???", clicked=enc.SetEntry(enc.all_entries[x]))
            else:
                ui.textbutton("???")

    # If locked buttons should not be visible. (No need for the "???" buttons.)
    elif enc.showLockedButtons == False:
        ui.textbutton(enc.unlocked_entries[x].name, clicked=enc.SetEntry(enc.unlocked_entries[x]))
        
        # Make a tag next to the button if it hasn't been viewed by the player yet.
        if not enc.unlocked_entries[x].status:
            ui.textbutton ("New!")
    ui.close()

def GenerateEntryListButtons(encyclopaedia):
    """
    Generates one textbutton for each encyclopaedia entry.
    
    Parameters:
        sencyclopaedia: The Encyclopaedia object to get data from
    """

    # If sorting by subject, display the subject heading and add an entry under it if it's the same subject
    if encyclopaedia.sorting_mode == encyclopaedia.SORT_SUBJECT:
        for x in range(len(encyclopaedia.subjects)):
            ui.text(encyclopaedia.subjects[x])
            for y in range(encyclopaedia.entry_list_size):  
                if encyclopaedia.get_entry_at(y).subject == encyclopaedia.subjects[x]:
                    generate_entry_button(y, encyclopaedia)   

    # If sorting by number, add the number next to the entry
    elif encyclopaedia.sorting_mode == encyclopaedia.SORT_NUMBER:    
        for x in range(encyclopaedia.entry_list_size):
            ui.hbox()
            ui.textbutton(str(encyclopaedia.get_entry_at(x).number))
            generate_entry_button(x, encyclopaedia)   
            ui.close()

    # If sorting Alphabetically or Reverse-Alphabetically, don't add anything before the entry
    else:
        for x in range(encyclopaedia.entry_list_size):
            generate_entry_eutton(x, encyclopaedia) 