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
        text enc.labels.unread_entry_label style "unread_entry_notice_text"


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
    if enc.sorting_mode == SortMode.SUBJECT:
        # Split entries by subject
        for key, group in groupby(enc.current_entries, attrgetter("subject")):
           text key style "encyclopaedia_list_subject_header" # The subject heading
           for entry in group:
               hbox:
                   use entry_button(enc, entry)

    elif enc.sorting_mode == SortMode.NUMBER:
        for entry in enc.current_entries:
            hbox:
                spacing 10
                text "{:02}".format(entry.number) style "encyclopaedia_list_number_text"
                use entry_button(enc, entry)

    # If sorting Alphabetically, Reverse-Alphabetically, or by Unread.
    else:
        if enc.nest_alphabetical_sort:
            # Split entries by first letter
            for key, group in groupby(enc.current_entries, key=lambda x: x.name[0]):
                text key style "encyclopaedia_list_letter_text"  # The letter heading
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

    # Active entries get shown automatically.
    # Ugly, but due to how ShowMenu() works, we need to put this on the screen,
    # not in an Action.
    # Generally, this is used by hyperlinks to jump directly to an EncEntry.
    on "show" action [
        If(enc.active, enc.SetEntry(enc.active)),
    ]

    frame:
        style_prefix "encyclopaedia"
        yfill True
        xsize 0.5

        vbox:
            frame:
                style_prefix "encyclopaedia"
                xfill True

                text enc.name

            frame:
                style_prefix "encyclopaedia"
                xfill True

                hbox:
                    xfill True
                    # Percentage unlocked display
                    text "[enc.labels.percentage_unlocked] Complete" style "encyclopaedia_header_text"

            frame:
                style_prefix "encyclopaedia"
                xfill True

                vbox:
                    spacing 2

                    text _("Filters") style "encyclopaedia_header_text"
                    hbox:
                        box_wrap True
                        xfill True
                        # Buttons to filter the entries that are displayed
                        textbutton _("All") action enc.ClearFilter() style "encyclopaedia_subject_filters_button"
                        for subject in enc.subjects:
                            textbutton subject action enc.FilterBySubject(subject) style "encyclopaedia_subject_filters_button"

                    hbox:
                        text _("Sort By") style "encyclopaedia_header_text"
                        hbox:
                            xfill False
                            # Buttons to sort entries.
                            textbutton "| [enc.labels.sort_number_label]" action enc.Sort(sorting_mode=SortMode.NUMBER) style_suffix "sort_by_button"
                            textbutton "| [enc.labels.sort_alphabetical_label]" action enc.Sort(sorting_mode=SortMode.ALPHABETICAL) style_suffix "sort_by_button"
                            textbutton "| [enc.labels.sort_reverse_alphabetical_label]" action enc.Sort(sorting_mode=SortMode.REVERSE_ALPHABETICAL) style_suffix "sort_by_button"
                            textbutton "| [enc.labels.sort_subject_label]" action enc.Sort(sorting_mode=SortMode.SUBJECT) style_suffix "sort_by_button"
                            textbutton "| [enc.labels.sort_unread_label] |" action enc.Sort(sorting_mode=SortMode.UNREAD) style_suffix "sort_by_button"

            vbox:
                hbox:
                    frame:
                        style_prefix "encyclopaedia"
                        ymaximum 1.0

                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            draggable True

                            ymaximum 0.80

                            vbox:
                                spacing 0
                                use vertical_list(enc) id "vertical list"

                frame:
                    style_prefix "encyclopaedia"
                    xfill True
                    yminimum 0.20

                    side "c r":

                        vbox:
                            yfill True

                            hbox:
                                # Buttons to show different styles of hiding locked data.
                                textbutton "View Locked Buttons" action enc.ToggleShowLockedButtons() style_suffix "sort_by_button"
                                textbutton "View Locked Entry" action enc.ToggleShowLockedEntry() style_suffix "sort_by_button"

                            hbox:
                                textbutton _("Return")  action [enc.CloseActiveEntry(), Return()]

                        null width 16


################################################################################
#    Encyclopaedia Entry:
#    Screen that's used to display an individual entry.
#
#    Args:
#        enc (Encyclopaedia): The encyclopaedia to use on this screen.
################################################################################
screen encyclopaedia_entry(enc):
    tag encyclopaedia_entry

    frame:
        style_prefix "encyclopaedia_entry"

        vbox:
            frame:
                style_prefix "encyclopaedia"
                xalign 1.0
                xfill True
                # Flavour text to indicate which entry we're currently on
                text enc.active.label

            frame:
                style_prefix "encyclopaedia"
                id "entry_nav"
                xalign 1.0
                hbox:
                    xfill True
                    # Previous / Next is relative to the sorting mode
                    textbutton _("Previous Entry") xalign .02 action enc.PreviousEntry() style "encyclopaedia_change_entry_button"
                    textbutton _("Next Entry") xalign .98 action enc.NextEntry() style "encyclopaedia_change_entry_button"

            vbox:
                spacing 8
                # If the entry or sub-entry has an image
                if enc.active.current_page.has_image:
                    frame:
                        style_prefix "encyclopaedia_image"

                        viewport:
                            scrollbars None
                            draggable True
                            mousewheel True
                            edgescroll (1.0, 1.0)
                            add enc.active.current_page.image

                frame:
                    style_prefix "encyclopaedia_entry_content"
                    id "entry_window"

                    if enc.active.current_page.has_image:
                        ymaximum 0.68
                    else:
                        ymaximum 0.845

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
                xalign 1.0
                xfill True

                if enc.active.has_pages:
                    hbox:
                        xfill True

                        # If there's a sub-entry, add Prev/Next Page buttons
                        textbutton _("Previous Page") xalign .02 action enc.PreviousPage() style "encyclopaedia_change_entry_button"

                        # Flavour text to indicate which sub-page out of the total is being viewed
                        text enc.labels.entry_current_page size 18 yalign 0.5

                        textbutton _("Next Page") xalign .98 action enc.NextPage() style "encyclopaedia_change_entry_button"

                else:
                    xpadding 10
                    ypadding 10
                    text " " size 18 yalign 0.5

            frame:
                style_prefix "encyclopaedia"
                xfill True

                hbox:
                    xfill True
                    # Flavour text that displays the current sorting mode
                    text "Sorting Mode: [enc.labels.sorting_mode]" xalign .02 size 18 yalign 0.5
                    textbutton _("Close Entry") id "close_entry_button" xalign .98 clicked enc.CloseActiveEntry() style "encyclopaedia_close_button"


########################
# Encyclopaedia Styles
########################
style encyclopaedia_vbox is vbox:
    spacing 6

style encyclopaedia_frame is frame:
    padding (6, 6, 6, 6)

style encyclopaedia_entry_frame is encyclopaedia_frame:
    xalign 1.0
    yalign 1.0

    xsize 0.5
    ysize 1.0

    padding (6, 6, 6, 6)

style encyclopaedia_entry_vbox is vbox:
    spacing 6

style encyclopaedia_entry_content_frame is encyclopaedia_frame:
    left_padding 6
    right_padding 6

    xalign 1.0

style encyclopaedia_image_frame is encyclopaedia_frame:
    xsize 1.0
    xalign 1.0
    ymaximum 0.5

style encyclopaedia_header_text:
    yalign 0.5

    size 20

style encyclopaedia_scrollbar is scrollbar

style encyclopaedia_vscrollbar is vscrollbar

style encyclopaedia_button is button

style encyclopaedia_button_text is button_text

style encyclopaedia_change_entry_button is button
style encyclopaedia_change_entry_button_text is button_text:
    size 18

style encyclopaedia_entry_button is encyclopaedia_button:
    xfill False

style encyclopaedia_entry_button_text is encyclopaedia_button_text:
    size 18

style encyclopaedia_list_letter_text:
    size 24
    padding (10, 10, 10, 10)
    yalign 0.5

style encyclopaedia_list_number_text:
    size 18
    padding (10, 10, 10, 10)
    yalign 0.5

style unread_entry_notice_text:
    size 18
    padding (10, 10, 10, 10)
    yalign 0.5

style encyclopaedia_entry_text is default:
    size 16

style encyclopaedia_list_subject_header:
    size 24

style encyclopaedia_subject_filters_button is encyclopaedia_button:
    xfill False

style encyclopaedia_subject_filters_button_text is encyclopaedia_button_text:
    size 18

style encyclopaedia_sort_by
style encyclopaedia_sort_by_button is encyclopaedia_button
style encyclopaedia_sort_by_button_text is encyclopaedia_button_text:
    size 18

style encyclopaedia_close_button is encyclopaedia_button
style encyclopaedia_close_button_text is encyclopaedia_button_text:
    size 18

############################
# Encyclopaedia Misc Setup
############################
init -1500:
    python:
        from itertools import groupby
        from operator import attrgetter
