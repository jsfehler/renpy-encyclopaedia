# Encyclopaedia Framework for Ren'Py
# Copyright 2014 Joshua Fehler <jsfehler@gmail.com>
# Last Updated: 10/26/2014
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
 #Function that creates the buttons for each entry.
 #It makes one button, based on the value "x", associated to the given encyclopaedia "enc".
 #Used in a "for loop" on a screen to generate the correct buttons for every entry 
    def generateEntryButton(x,enc):  
        ui.hbox()
        if enc.showLockedButtons:
            if enc.all_entries[x][1].locked == False: #If the entry is unlocked, make the button to go to it. If it's locked, make an inactive "???" button
                ui.textbutton(enc.all_entries[x][1].name, clicked= [ enc.ChangeStatus(x), enc.SetEntry(x), Show("encyclopaedia_entry")] )
                if enc.all_entries[x][1].status == None or enc.all_entries[x][1].status == False:
                    ui.textbutton ("New!")
          
            else: #If locked entries should be shown in the list, the "???" button should go to the entry. If not, it's an inactive button
                if enc.showLockedEntry:
                    ui.textbutton("???", clicked=[ enc.ChangeStatus(x), enc.SetEntry(x), Show("encyclopaedia_entry")])
                else:
                    ui.textbutton("???")
    
        if enc.showLockedButtons == False: #Only showing unlocked entries in this case, no need for the "???" button
            ui.textbutton(enc.unlocked_entries[x][1].name, clicked= [ enc.ChangeStatus(x), enc.SetEntry(x), Show("encyclopaedia_entry")] )
            if enc.unlocked_entries[x][1].status == None or enc.unlocked_entries[x][1].status == False:  
                ui.textbutton ("New!")
        ui.close()

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
                    text encyclopaedia.getPercentageUnlocked() + " Complete" #Percentage display

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
                        text encyclopaedia.sortingMode xalign 0.5 #Flavour text to display the current sorting mode.
     
                        python:
                            #If sorting by subject, display the subject heading and add an entry under it if it's the same subject
                            if encyclopaedia.sortingMode == "Subject":
                                for x in range(len(encyclopaedia.subjects) ):
                                    ui.text(encyclopaedia.subjects[x])
                                    for y in range(encyclopaedia.entry_list_size):  
                                        if encyclopaedia.getEntry(y).subject == encyclopaedia.subjects[x]:
                                            generateEntryButton(y,encyclopaedia)   
       
                            #If sorting by number, add the number next to the entry
                            elif encyclopaedia.sortingMode == "Number":    
                                for x in range(encyclopaedia.entry_list_size):
                                    ui.hbox()
                                    ui.textbutton (str(encyclopaedia.getEntry(x).number))
                                    generateEntryButton(x,encyclopaedia)   
                                    ui.close()
      
                            #If sorting Alphabetically or Reverse-Alphabetically, don't add anything before the entry
                            else:
                                for x in range(encyclopaedia.entry_list_size):
                                    generateEntryButton(x,encyclopaedia) 
    
    frame:
        xalign .98
        yalign .98
        vbox:
            textbutton "Sort by Number" action encyclopaedia.Sort(sorting_mode="Number") #Buttons to sort entries
            textbutton "Sort A to Z" action encyclopaedia.Sort(sorting_mode="A to Z")
            textbutton "Sort Z to A" action encyclopaedia.Sort(sorting_mode="Z to A")
            textbutton "Sort by Subject" action encyclopaedia.Sort(sorting_mode="Subject")
   
            textbutton "Show/Hide Locked Buttons" action encyclopaedia.ToggleShowLockedButtons()
            textbutton "Show/Hide Locked Entry" action encyclopaedia.ToggleShowLockedEntry()
   
            #Sort and SaveStatus are unnecessary if you're not using persistent data
            textbutton "Return"  action [encyclopaedia.Sort(sorting_mode="Number"), encyclopaedia.SaveStatus(persistent.new_dict, "new_0"), Return()] #Sorting mode has to be number to save properly. "new_0" needs to be the prefix for the persistent dictionary.

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
                $page_indicator = "0%d : %s" % (encyclopaedia.getEntryData()[1].number, encyclopaedia.getEntryData()[1].getName()) # Flavour text to indicate which page we're current on
                text page_indicator
  
            frame:
                id "entry_nav"
                style_group "mm_root"
                xfill True
                xmargin 10
                hbox:
                    xfill True
                    textbutton "Previous Entry" xalign .02 action encyclopaedia.PreviousEntry() #Relative to the sorting mode
                    textbutton "Next Entry" xalign .98 action encyclopaedia.NextEntry() #Relative to the sorting mode  
       
            hbox:
                $ddd = config.screen_width
                $dd = config.screen_width/2
                $pp = config.screen_height/2
                if encyclopaedia.getEntryData()[1].hasImage: #If the entry or sub-entry has an image, add it to the screen   
                    frame:
                        xmargin 10
                        yfill True
                        xfill True

                        xmaximum dd
                        ymaximum pp  

                        $current_image = encyclopaedia.getEntryData()[1].getImage()
                        add current_image crop (0,10,dd-30,pp-10)
   
                window:
                    id "entry_window"
                    xmargin 10
                    xfill True
                    yfill True
                    xalign 0.5
                    xmaximum ddd
                    ymaximum pp
                    viewport:
                        scrollbars "vertical"
                        mousewheel True  
                        draggable True
                        xfill True
                        yfill True  
                        vbox:
                            spacing 15
                            for item in encyclopaedia.entry_text: #entry_text is a list of paragraphs from what whatever the current entry is
                                text item

            frame:
                style_group "mm_root"  
                xfill True
                yfill False
                xmargin 10
   
                hbox:
                    xfill True  
  
                    if encyclopaedia.getEntryData()[1].hasSubEntry: #If there's a sub-entry, add Prev/Next Page buttons     
                        textbutton "Previous Page" xalign .02 action encyclopaedia.PreviousPage()

                        text "Page %d / %d" % (encyclopaedia.sub_current_position, encyclopaedia.getEntryData()[1].pages) #Flavour text to indicate which sub-page is being viewed

                        textbutton "Next Page" xalign .98 action encyclopaedia.NextPage()  
 
                    else:
                        text("")
 
        frame:
            xfill True
            xmargin 10

            yalign .98
            hbox:
                xfill True
                text "Sorting Mode: %s" % (encyclopaedia.sortingMode,) #Flavour text that displays the current sorting mode
                textbutton "Close Entry" id "close_entry_button" xalign .98 clicked [encyclopaedia.ResetSubPage(), Show("encyclopaedia_list")] 

##############################################################################
# Encyclopaedia Button
#
# Contains a button to open the encyclopaedia at any time during the game
screen show_enc_button:
    textbutton "Open Encyclopaedia" xalign .98 yalign .02 action ShowMenu("encyclopaedia_list")
 
# The game starts here.
label start:
 
    show screen show_enc_button   
  
    "Do you want to add entries 4 and 6?" 

    #Unlocking an entry during the game requires the lock flag to be set to False, and then the encyclopaedia to be updated.
    menu:
        "Yes":
            $ persistent.en6_locked = False
            $ encyclopaedia.unlockEntry(en6, persistent.en6_locked)
   
            $ persistent.en4_locked = False  
            $ encyclopaedia.unlockEntry(en4, persistent.en4_locked)
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
            $ encyclopaedia.unlockEntry(en7, persistent.en7_locked)
            "Done."
        "No":
            "How was it?"
            
    return