################################################################################
#    Entry Button:
#    Sub-screen to determine what sort of button to show for any given entry in a list of entries.
#    Used by the vertical_list sub-screen.
#
#    Determining which button to show for the entry is based on the following factors:
#       - Should locked buttons be displayed?
#           - If yes, the button to show depends on:
#               - If the entry is unlocked, add a button with the correct label and link
#               - If the entry is locked, then:
#                   - If locked entries should be accessible, add a button with the correct label and link.
#                   - If locked entries should not be accessible, add a disabled button
#           - If no, simply add a button with the correct label and link, knowing only unlocked entries are being fed in
#
#    Args:
#        enc (Encyclopaedia): The encyclopaedia to use on this screen.
#        entry (EncEntry): The entry to associate with the button.
################################################################################
screen entry_button(enc, entry):
    textbutton entry.name action enc.SetEntry(entry) style "encyclopaedia_entry_button"

    if (entry.locked is False) and (not entry.viewed):
        text enc.labels.unread_entry_label


################################################################################
#    Vertical List:
#    Sub-screen that displays a vertical list of entry buttons.
#    The way entry buttons are displayed depends on the Encyclopaedia's sorting mode.
#    Used by the encyclopaedia_list screen.
#
#    Args:
#        enc (Encyclopaedia): The encyclopaedia to use on this screen.
################################################################################
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


################################################################################
#    Encyclopaedia List:
#    Screen that's used to display the list of entries, the filter buttons, and the sorting buttons
#
#    Args:
#        enc (Encyclopaedia): The encyclopaedia to use on this screen.
################################################################################
screen encyclopaedia_list(enc):
    tag menu
    modal True

    frame:
        style_prefix "encyclopaedia"

        vbox:
            spacing 10

            frame:
                style_prefix "encyclopaedia"
                xfill True

                text "Welcome to the Demo Encyclopaedia"

            frame:
                style_prefix "encyclopaedia"
                xfill True

                hbox:
                    xfill True
                    # Percentage unlocked display
                    text "{} Complete".format(enc.labels.percentage_unlocked)

            frame:
                style_prefix "encyclopaedia"
                xfill True

                vbox:
                    text "Filters"
                    hbox:
                        xfill True
                        # Buttons to filter the entries that are displayed
                        textbutton "All" action enc.ClearFilter() style "encyclopaedia_button"
                        for subject in enc.subjects:
                            textbutton subject action enc.FilterBySubject(subject) style "encyclopaedia_button"

            hbox:
                frame:
                    style_prefix "encyclopaedia"
                    yfill True
                    xmaximum 600
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
                    style_prefix "encyclopaedia"
                    xfill True
                    bottom_margin 10
                    yalign 1.0

                    vbox:
                        # Buttons to sort entries.
                        textbutton "Sort by {}".format(enc.labels.sort_number_label) action enc.Sort(sorting_mode=enc.SORT_NUMBER) xfill True
                        textbutton "Sort by {}".format(enc.labels.sort_alphabetical_label) action enc.Sort(sorting_mode=enc.SORT_ALPHABETICAL) xfill True
                        textbutton "Sort by {}".format(enc.labels.sort_reverse_alphabetical_label) action enc.Sort(sorting_mode=enc.SORT_REVERSE_ALPHABETICAL) xfill True
                        textbutton "Sort by {}".format(enc.labels.sort_subject_label) action enc.Sort(sorting_mode=enc.SORT_SUBJECT) xfill True
                        textbutton "Sort by {}".format(enc.labels.sort_unread_label) action enc.Sort(sorting_mode=enc.SORT_UNREAD) xfill True

                        # Buttons to show different styles of hiding locked data.
                        textbutton "Show/Hide Locked Buttons" action enc.ToggleShowLockedButtons() xfill True
                        textbutton "Show/Hide Locked Entry" action enc.ToggleShowLockedEntry() xfill True

                        textbutton "Return"  action [Hide("encyclopaedia_list"), Return()] xfill True


################################################################################
#    Encyclopaedia Entry:
#    Screen that's used to display an individual entry.
#
#    Args:
#        enc (Encyclopaedia): The encyclopaedia to use on this screen.
################################################################################
screen encyclopaedia_entry(enc):
    tag menu
    modal True

    frame:
        style_prefix "encyclopaedia"

        vbox:
            spacing 10

            frame:
                style_prefix "encyclopaedia"
                xfill True
                # Flavour text to indicate which entry we're currently on
                text enc.active.label

            frame:
                style_prefix "encyclopaedia"
                id "entry_nav"
                xfill True
                hbox:
                    xfill True
                    # Previous / Next is relative to the sorting mode
                    textbutton "Previous Entry" xalign .02 action enc.PreviousEntry() style "encyclopaedia_button"
                    textbutton "Next Entry" xalign .98 action enc.NextEntry() style "encyclopaedia_button"

            hbox:
                spacing 10
                # If the entry or sub-entry has an image
                if enc.active.current_page.has_image:
                    frame:
                        style_prefix "encyclopaedia_image"

                        xsize 0.5
                        ysize 734

                        viewport:
                            scrollbars None
                            draggable True
                            mousewheel True
                            edgescroll (1.0, 1.0)
                            add enc.active.current_page.image

                frame:
                    style_prefix "encyclopaedia"
                    id "entry_window"
                    yfill False
                    ysize 734
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vbox:
                            spacing 0
                            # Display the current entry's text
                            for item in enc.active.current_page.text:
                                text "[item]" style "encyclopaedia_entry_text"


            frame:
                style_prefix "encyclopaedia"
                xfill True
                #yfill True

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
                    ypadding 14
                    text " "

            frame:
                style_prefix "encyclopaedia"
                xfill True

                hbox:
                    xfill True
                    # Flavour text that displays the current sorting mode
                    text "Sorting Mode: {}".format(enc.labels.sorting_mode)
                    textbutton "Close Entry" id "close_entry_button" xalign .98 clicked [enc.ResetSubPage(), Show("encyclopaedia_list", None, enc)] style "encyclopaedia_button"


########################
# Encyclopaedia Styles
########################
style encyclopaedia_frame is frame

style encyclopaedia_image_frame is encyclopaedia_frame:
    yfill True
    xfill True
    xmaximum half_screen_width
    ymaximum half_screen_height

style encyclopaedia_scrollbar is scrollbar

style encyclopaedia_vscrollbar is vscrollbar

style encyclopaedia_button is button

style encyclopaedia_button_text is button_text

style encyclopaedia_entry_button is encyclopaedia_button:
    xfill False

style encyclopaedia_entry_button_text is encyclopaedia_button_text

style encyclopaedia_entry_text is default:
    size 18


############################
# Encyclopaedia Misc Setup
############################
init -1500:
    python:
        from itertools import groupby
        from operator import attrgetter

        half_screen_width = config.screen_width / 2
        half_screen_height = config.screen_height / 2
