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
                    text encyclopaedia.labels.percentage_unlocked + " Complete"

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
                        # Flavour text to display the current sorting mode.
                        text encyclopaedia.labels.sorting_mode xalign 0.5
     
                        python:
                            # Utility function that generates all the buttons used to access the Entries.
                            generate_entry_list_buttons(encyclopaedia)

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
   
            #Sort and SaveStatus are unnecessary if you're not using persistent data (ie: if the encyclopaedia is save game independent)
            #Sorting mode has to be by Number to save properly. "new_0" should be whatever the prefix you choose for the persistent dictionary is.
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
                $ entry_indicator = "0%d : %s" % (encyclopaedia.active.number, encyclopaedia.active.name)
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
                # If the entry or sub-entry has an image
                if encyclopaedia.active.has_image:
                    frame:
                        xmargin 10
                        yfill True
                        xfill True

                        xmaximum half_screen_width
                        ymaximum half_screen_height  

                        # You don't have to crop your images. I just did this for the example.
                        # You can position them however you want.
                        $current_image = encyclopaedia.active.image
                        add current_image crop (0, 10, half_screen_width - 30, half_screen_height - 10)
   
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
                                for item in encyclopaedia.active.current_page.text:
                                    text item
                
                # If there's no image                        
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
                                for item in encyclopaedia.active.current_page.text:
                                    text item

            frame:
                style_group "mm_root"  
                xfill True
                yfill False
                xmargin 10
                hbox:
                    xfill True  
  
                    # If there's a sub-entry, add Prev/Next Page buttons
                    if encyclopaedia.active.has_sub_entry:    
                        textbutton "Previous Page" xalign .02 action encyclopaedia.PreviousPage()

                        # Flavour text to indicate which sub-page out of the total is being viewed
                        text encyclopaedia.labels.entry_current_page

                        textbutton "Next Page" xalign .98 action encyclopaedia.NextPage()  
 
                    else:
                        text("")
 
        frame:
            xfill True
            xmargin 10

            yalign .98
            hbox:
                xfill True
                # Flavour text that displays the current sorting mode
                text "Sorting Mode: %s" % encyclopaedia.labels.sorting_mode
                textbutton "Close Entry" id "close_entry_button" xalign .98 clicked [encyclopaedia.Sort(), encyclopaedia.ResetSubPage(), Show("encyclopaedia_list")] 
