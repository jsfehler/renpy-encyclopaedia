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

init -1 python:
    from encyclopaedia.encyclopaedia import Encyclopaedia
    from encyclopaedia.encentry import EncEntry

    def generateEntryButton(x, enc, entry_screen):
        """ 
        Create a button for an Entry in an Encyclopaedia.
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
            if enc.all_entries[x][1].locked == False:
                ui.textbutton(enc.all_entries[x][1].name, clicked=[enc.ChangeStatus(enc.all_entries[x]), 
                                                                   enc.SetEntry(enc.all_entries[x]), 
                                                                   Show(entry_screen)])
                
                # Make a tag next to the button if it hasn't been viewed by the player yet.
                if not enc.all_entries[x][1].status:    
                    ui.textbutton ("New!")

            else:
                # If locked entries should be viewable, the "???" button should go to the entry. 
                # If not, it's an inactive button.
                if enc.showLockedEntry:
                    ui.textbutton("???", clicked=[enc.ChangeStatus(enc.all_entries[x]), 
                                                  enc.SetEntry(enc.all_entries[x]), 
                                                  Show(entry_screen)])
                else:
                    ui.textbutton("???")
    
        # If locked buttons should not be visible. (No need for the "???" buttons.)
        elif enc.showLockedButtons == False:
            ui.textbutton(enc.unlocked_entries[x][1].name, clicked=[enc.ChangeStatus(enc.unlocked_entries[x]), 
                                                                    enc.SetEntry(enc.unlocked_entries[x]), 
                                                                    Show(entry_screen)] )
            
            # Make a tag next to the button if it hasn't been viewed by the player yet.
            if not enc.unlocked_entries[x][1].status:
                ui.textbutton ("New!")
        ui.close()

    def generateEntryList(show_screen=""):
        # If sorting by subject, display the subject heading and add an entry under it if it's the same subject
        if encyclopaedia.sorting_mode == encyclopaedia.SORT_SUBJECT:
            for x in range(len(encyclopaedia.subjects)):
                ui.text(encyclopaedia.subjects[x])
                for y in range(encyclopaedia.entry_list_size):  
                    if encyclopaedia.get_entry_at(y).subject == encyclopaedia.subjects[x]:
                        generateEntryButton(y, encyclopaedia, show_screen)   

        # If sorting by number, add the number next to the entry
        elif encyclopaedia.sorting_mode == encyclopaedia.SORT_NUMBER:    
            for x in range(encyclopaedia.entry_list_size):
                ui.hbox()
                ui.textbutton (str(encyclopaedia.get_entry_at(x).number + 1))
                generateEntryButton(x, encyclopaedia, show_screen)   
                ui.close()

        # If sorting Alphabetically or Reverse-Alphabetically, don't add anything before the entry
        else:
            for x in range(encyclopaedia.entry_list_size):
                generateEntryButton(x, encyclopaedia, show_screen) 
        
##############################################################################
# Encyclopaedia List
#
# Screen that's used to display the list of entries 
screen encyclopaedia_list:
    tag menu
 
    window:
        style "gm_root"

        vbox:
            spacing 10
  
            frame:
                style_group "mm_root"
                xfill True
                xmargin 10
                top_margin 10
                text "Welcome to the Demo Encyclopaedia"
    
            frame:
                style_group "mm_root"
                xfill True
                xmargin 10
    
                hbox:
                    xfill True
                    # Percentage unlocked display
                    text encyclopaedia.get_percentage_unlocked_label() + " Complete"

            frame:
                style_group "mm_root"  
                xmargin 10
                yfill True
                xmaximum 400
                bottom_margin 10
   
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    vbox: 
                        #Flavour text to display the current sorting mode.
                        text encyclopaedia.sorting_mode_label xalign 0.5
     
                        python:
                            generateEntryList(show_screen="encyclopaedia_entry")

    frame:
        xalign .98
        yalign .98
        vbox:
            # Buttons to sort entries.
            textbutton "Sort by Number" action encyclopaedia.Sort(sorting_mode=encyclopaedia.SORT_NUMBER)
            textbutton "Sort A to Z" action encyclopaedia.Sort(sorting_mode=encyclopaedia.SORT_ALPHABETICALLY)
            textbutton "Sort Z to A" action encyclopaedia.Sort(sorting_mode=encyclopaedia.SORT_REVERSE_ALPHABETICALLY)
            textbutton "Sort by Subject" action encyclopaedia.Sort(sorting_mode=encyclopaedia.SORT_SUBJECT)
            textbutton "Sort by Unread" action encyclopaedia.Sort(sorting_mode=encyclopaedia.SORT_UNREAD)
   
            # Debug buttons to show off different styles of hiding locked data.
            textbutton "Show/Hide Locked Buttons" action encyclopaedia.ToggleShowLockedButtons()
            textbutton "Show/Hide Locked Entry" action encyclopaedia.ToggleShowLockedEntry()
   
            #Sort and SaveStatus are unnecessary if you're not using persistent data
            #Sorting mode has to be by Number to save properly. "new_0" should be whatever the prefix for the persistent dictionary is.
            textbutton "Return"  action [encyclopaedia.Sort(sorting_mode=encyclopaedia.SORT_NUMBER), 
                                                            encyclopaedia.SaveStatus(persistent.new_dict, "new_0"), 
                                                            Return()]

##############################################################################
# Encyclopaedia Entry
#
# Screen that's used to display each entry 
screen encyclopaedia_entry:
    tag menu
 
    window:
        style "gm_root"  

        xfill True
        yfill True
        vbox:
            spacing 10
  
            frame:
                style_group "mm_root"
                xfill True
                xmargin 10
                top_margin 10
                # Flavour text to indicate which entry we're currently on
                $ entry_indicator = "0%d : %s" % (encyclopaedia.index.number + 1, encyclopaedia.index.name)
                text entry_indicator
  
            frame:
                id "entry_nav"
                style_group "mm_root"
                xfill True
                xmargin 10
                hbox:
                    xfill True
                    textbutton "Previous Entry" xalign .02 action encyclopaedia.PreviousEntry() # Relative to the sorting mode
                    textbutton "Next Entry" xalign .98 action encyclopaedia.NextEntry() # Relative to the sorting mode  
       
            hbox:
                $ half_screen_width = config.screen_width / 2
                $ half_screen_height = config.screen_height / 2
                # If the entry or sub-entry has an image, add it to the screen
                if encyclopaedia.index.has_image:
                    frame:
                        xmargin 10
                        yfill True
                        xfill True

                        xmaximum half_screen_width
                        ymaximum half_screen_height  

                        $current_image = encyclopaedia.index.image
                        add current_image crop (0, 10, half_screen_width-30, half_screen_height-10)
   
                    window:
                        id "entry_window"
                        xmargin 10
                        xfill True
                        yfill True
                        xmaximum config.screen_width
                        ymaximum half_screen_height
                        viewport:
                            scrollbars "vertical"
                            mousewheel True  
                            draggable True
                            xfill True
                            yfill True  
                            vbox:
                                spacing 15
                                # Display the current entry's text
                                for item in encyclopaedia.index.current_page.text:
                                    text item
                                        
                else:
                    window:
                        id "entry_window"
                        xmargin 10
                        xfill True
                        yfill True
                        xmaximum config.screen_width
                        ymaximum half_screen_height
                        viewport:
                            scrollbars "vertical"
                            mousewheel True  
                            draggable True
                            xfill True
                            yfill True  
                            vbox:
                                spacing 15
                                xfill True
                                yfill True 
                                # Display the current entry's text
                                for item in encyclopaedia.index.current_page.text:
                                    text item

            frame:
                style_group "mm_root"  
                xfill True
                yfill False
                xmargin 10
                hbox:
                    xfill True  
  
                    # If there's a sub-entry, add Prev/Next Page buttons
                    if encyclopaedia.index.has_sub_entry:    
                        textbutton "Previous Page" xalign .02 action encyclopaedia.PreviousPage()

                        # Flavour text to indicate which sub-page out of the total is being viewed
                        text encyclopaedia.get_entry_current_page_label(label="Page")

                        textbutton "Next Page" xalign .98 action encyclopaedia.NextPage()  
 
                    else:
                        text("")
 
        frame:
            xfill True
            xmargin 10

            yalign .98
            hbox:
                xfill True
                text "Sorting Mode: %s" % encyclopaedia.sorting_mode_label #Flavour text that displays the current sorting mode
                textbutton "Close Entry" id "close_entry_button" xalign .98 clicked [encyclopaedia.Sort(), encyclopaedia.ResetSubPage(), Show("encyclopaedia_list")] 

##############################################################################
# Encyclopaedia Button
# Contains a button to open the encyclopaedia at any time during the game
screen show_enc_button:
    textbutton "Open Encyclopaedia" xalign .98 yalign .02 action ShowMenu("encyclopaedia_list")
 
# The game starts here.
label start:
 
    show screen show_enc_button   
  
    "Do you want to add entries 4 and 6?" 

    # Unlocking an entry during the game requires the lock flag to be set to False, and then the encyclopaedia to be updated.
    menu:
        "Yes":
            $ persistent.en6_locked = False
            $ encyclopaedia.unlock_entry(en6, persistent.en6_locked)
   
            $ persistent.en4_locked = False  
            $ encyclopaedia.unlock_entry(en4, persistent.en4_locked)
            "Ok, they're in. How about the sub-entries?" 
   
            menu:
                "Add Sub-Entry 6-2 and 6-3":
                    $ persistent.en6_2_locked = False   
                    $ en6.unlockSubEntry(en6_2, persistent.en6_2_locked)
                    $ persistent.en6_3_locked = False  
                    $ en6.unlockSubEntry(en6_3, persistent.en6_3_locked)

                "Add Sub-Entry 2-3":
                    $ persistent.en2_3_locked = False   
                    $ en2.unlockSubEntry(en2_3, persistent.en2_3_locked)
   
                "Don't Add Sub-Entry":
                    "Ok"  
   
        "No":
            "They weren't added." 
   
    "How about entry 7?"
    menu:
        "Yes":
            $ persistent.en7_locked = False  
            $ encyclopaedia.unlock_entry(en7, persistent.en7_locked)
            "Done."
        "No":
            "How was it?"
            
    return