##############################################################################
# Entry Button
#
# Sub-screen which determines what sort of button to show for an entry.
# Args:
#   enc (Encyclopaedia): The encyclopaedia to use on this screen.
#   entry (EncEntry): The entry to associate with the button.
screen entry_button(enc, entry):
    if enc.show_locked_buttons:

        # If the entry is unlocked, add an active button.
        if entry.locked is False:
            textbutton entry.name action enc.SetEntry(entry) style "encyclopaedia_button"

            # Add tag next to the button, if it hasn't been viewed yet.
            if not entry.viewed:
                text enc.labels.unread_entry_label

        # If the entry is locked, add a button depending on what should be shown.
        else:
            if enc.show_locked_entry:
                textbutton enc.labels.locked_entry_label action enc.SetEntry(entry) style "encyclopaedia_button"
            else:
                textbutton enc.labels.locked_entry_label style "encyclopaedia_button"

    # Else, if locked buttons should not be visible then no need for placeholders.
    elif enc.show_locked_buttons is False:
        textbutton entry.name action enc.SetEntry(entry) style "encyclopaedia_button"

        # Add tag next to the button, if it hasn't been viewed yet.
        if not entry.viewed:
            text enc.labels.unread_entry_label

##############################################################################
# Vertical List
#
# Sub-screen which displays a vertical list of buttons.
# Args:
#   enc (Encyclopaedia): The encyclopaedia to use on this screen.
screen vertical_list(enc):
    # The list used is chosen based on if we want to show locked entries on
    #   the entry select screen or not.

    if enc.sorting_mode == enc.SORT_SUBJECT:
        # Split entries by subject
        for key, group in groupby(enc.current_entries, attrgetter("subject")):
           text key  # The subject heading
           for entry in group:
               hbox:
                   use entry_button(enc, entry)

    elif enc.sorting_mode == enc.SORT_NUMBER:
        for entry in enc.current_entries:
            hbox:
                spacing 10
                text "{:02}".format(entry.number)
                use entry_button(enc, entry)

    # If sorting Alphabetically, Reverse-Alphabetically, or by Unread.
    else:
        if enc.nest_alphabetical_sort:
            # Split entries by first letter
            for key, group in groupby(enc.current_entries, key=lambda x: x.name[0]):
                text key  # The letter heading
                for entry in group:
                    hbox:
                        use entry_button(enc, entry)

        else:
            for entry in enc.current_entries:
                hbox:
                    use entry_button(enc, entry)

##############################################################################
# Encyclopaedia List
#
# Screen that's used to display the list of entries.
# Args:
#   enc (Encyclopaedia): The encyclopaedia to use on this screen.
screen encyclopaedia_list(enc):
    tag menu
    modal True

    window:
        style "encyclopaedia_window"

        vbox:
            spacing 10
  
            frame:
                style "encyclopaedia"
                xfill True

                text "Welcome to the Demo Encyclopaedia"
    
            frame:
                style "encyclopaedia"
                xfill True
    
                hbox:
                    xfill True
                    # Percentage unlocked display
                    text "{} Complete".format(enc.labels.percentage_unlocked)

            frame:
                style "encyclopaedia"
                xfill True

                hbox:
                    xfill True
                    # Percentage unlocked display
                    textbutton "All" action enc.ClearFilter() style "encyclopaedia_button"
                    for subject in enc.subjects:
                        textbutton subject action enc.FilterBySubject(subject) style "encyclopaedia_button"

            hbox:
                frame:
                    style "encyclopaedia"
                    yfill True
                    xmaximum 400
                    bottom_margin 10

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vbox:
                            # Flavour text to display the current sorting mode.
                            text enc.labels.sorting_mode xalign 0.5

                            use vertical_list(enc) id "vertical list"

                frame:
                    style "encyclopaedia"
                    xfill True
                    bottom_margin 10
                    yalign 0.95

                    vbox:
                        # Buttons to sort entries.
                        textbutton "Sort by %s" % enc.labels.sort_number_label action enc.Sort(sorting_mode=enc.SORT_NUMBER) style "encyclopaedia_button"
                        textbutton "Sort by %s" % enc.labels.sort_alphabetical_label action enc.Sort(sorting_mode=enc.SORT_ALPHABETICAL) style "encyclopaedia_button"
                        textbutton "Sort by %s" % enc.labels.sort_reverse_alphabetical_label action enc.Sort(sorting_mode=enc.SORT_REVERSE_ALPHABETICAL) style "encyclopaedia_button"
                        textbutton "Sort by %s" % enc.labels.sort_subject_label action enc.Sort(sorting_mode=enc.SORT_SUBJECT) style "encyclopaedia_button"
                        textbutton "Sort by %s" % enc.labels.sort_unread_label action enc.Sort(sorting_mode=enc.SORT_UNREAD) style "encyclopaedia_button"

                        # Buttons to show different styles of hiding locked data.
                        textbutton "Show/Hide Locked Buttons" action enc.ToggleShowLockedButtons() style "encyclopaedia_button"
                        textbutton "Show/Hide Locked Entry" action enc.ToggleShowLockedEntry() style "encyclopaedia_button"

                        # Sort and SaveStatus are unnecessary if you're not using persistent data (ie: if the encyclopaedia is save game independent)
                        # Sorting mode has to be by Number to save properly. "new_0" should be whatever the prefix you choose for the persistent dictionary is.
                        textbutton "Return"  action [enc.Sort(sorting_mode=enc.default_sorting_mode),
                                                     enc.SaveStatus(persistent.new_status, "new"),
                                                     Hide("encyclopaedia_list"),
                                                     Return()] style "encyclopaedia_button"

##############################################################################
# Encyclopaedia Entry
#
# Screen that's used to display each entry.
# Args:
#   enc (Encyclopaedia): The encyclopaedia to use on this screen.
screen encyclopaedia_entry(enc):
    tag menu
 
    window:
        style "encyclopaedia_window"
        xfill True
        yfill True

        vbox:
            spacing 10
  
            frame:
                style "encyclopaedia"
                xfill True
                # Flavour text to indicate which entry we're currently on
                text enc.active.label
  
            frame:
                style "encyclopaedia"
                id "entry_nav"
                xfill True
                hbox:
                    xfill True
                    # Previous / Next is relative to the sorting mode
                    textbutton "Previous Entry" xalign .02 action enc.PreviousEntry() style "encyclopaedia_button"
                    textbutton "Next Entry" xalign .98 action enc.NextEntry() style "encyclopaedia_button"
       
            hbox:
                $ half_screen_width = config.screen_width / 2
                $ half_screen_height = config.screen_height / 2

                # If the entry or sub-entry has an image
                if enc.active.current_page.has_image:
                    frame:
                        style "encyclopaedia"
                        yfill True
                        xfill True

                        xmaximum half_screen_width
                        ymaximum half_screen_height

                        viewport:
                            scrollbars True
                            draggable True
                            mousewheel True
                            edgescroll (1.0, 1.0)
                            add enc.active.current_page.image
   
                    window:
                        style "encyclopaedia"
                        id "entry_window"
                        xfill True
                        yfill True
                        xmaximum half_screen_width
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
                                for item in enc.active.current_page.text:
                                    text item

                # If there's no image                        
                else:
                    window:
                        style "encyclopaedia"
                        id "entry_window"
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
                                for item in enc.active.current_page.text:
                                    text item

            frame:
                style "encyclopaedia"
                xfill True
                yfill False

                if enc.active.has_sub_entry:
                    hbox:
                        xfill True

                        # If there's a sub-entry, add Prev/Next Page buttons
                        textbutton "Previous Page" xalign .02 action enc.PreviousPage() style "encyclopaedia_button"

                        # Flavour text to indicate which sub-page out of the total is being viewed
                        text enc.labels.entry_current_page

                        textbutton "Next Page" xalign .98 action enc.NextPage() style "encyclopaedia_button"

                else:
                    xpadding 10
                    ypadding 10
                    text " "

        frame:
            style "encyclopaedia"
            xfill True

            yalign .98
            hbox:
                xfill True
                # Flavour text that displays the current sorting mode
                text "Sorting Mode: %s" % enc.labels.sorting_mode
                textbutton "Close Entry" id "close_entry_button" xalign .98 clicked [enc.ResetSubPage(), Show("encyclopaedia_list", None, enc)] style "encyclopaedia_button"

init -1500:
    python:
        from itertools import groupby
        from operator import attrgetter

        style.encyclopaedia = Style(style.default)

        style.encyclopaedia_window.background = "#333333"

        style.encyclopaedia.background = "#6C5A49"
        style.encyclopaedia.color = "#666"
        style.encyclopaedia.hover_color = "#C7C7A6"
        style.encyclopaedia.selected_color = "#C7C7A6"
        style.encyclopaedia.size = 16
        style.encyclopaedia.padding = (8, 8)
        style.encyclopaedia.xmargin = 8
        style.encyclopaedia.top_margin = 8

        style.encyclopaedia_button.background = "#AA8F66"
        style.encyclopaedia_button.hover_background = "#FFA552"
        style.encyclopaedia_button.insensitive_background = "#8B1E3F"
        style.encyclopaedia_button_text.color = "#483C46"
        style.encyclopaedia_button_text.insensitive_color = "#1C0221"
