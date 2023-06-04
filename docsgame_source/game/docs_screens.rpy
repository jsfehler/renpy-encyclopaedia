################################################################################
#    Encyclopaedia Entry:
#    Screen that's used to display an individual EncEntry.
#
#    Args:
#        enc (Encyclopaedia): The encyclopaedia to use on this screen.
################################################################################
screen docs_entry(enc):
    tag encyclopaedia_entry

    frame:
        style_prefix "encyclopaedia_entry"

        vbox:
            # Flavour text to indicate which entry we're currently on.
            frame:
                style_suffix "label_frame"

                text enc.active.label

            # Buttons to swap between pages.
            frame:
                style_suffix "change_entry_frame"
                id "entry_nav"

                hbox:
                    style_suffix "change_entry_hbox"

                    # Previous / Next is relative to the sorting mode
                    textbutton _("Previous Entry") xalign .02 action enc.PreviousEntry() style_suffix "change_entry_button"
                    textbutton _("Next Entry") xalign .98 action enc.NextEntry() style_suffix "change_entry_button"

            # Entry text
            vbox:
                spacing 8
                # If the entry has an image
                if enc.active.current_page.has_image:
                    frame:
                        style_prefix "encyclopaedia_entry_image"

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
                        ymaximum 0.685
                    else:
                        ymaximum 0.846

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vbox:
                            spacing 16
                            # Display the current entry's text
                            $ current_parent = None
                            for element in enc.active.current_page.elements:
                                if element.name == 'code':
                                    use code_block(element)

                                elif element.name == 'ul':
                                    use inside_ul(element)
                                    $ current_parent = element

                                elif element.name == 'ol':
                                    use inside_ol(element)
                                    $ current_parent = element

                                elif current_parent:
                                    if element in current_parent.children:
                                        if current_parent.name == 'ul':
                                            use inside_ul(element)

                                        elif current_parent.name == 'ol':
                                            use inside_ol(element)

                                        else:
                                            text "[element.text]" style element.style

                                    else:
                                        $ current_parent = None
                                        text "[element.text]" style element.style

                                else:
                                    text "[element.text]" style element.style

            frame:
                style_prefix "encyclopaedia"
                xalign 1.0
                xfill True

                # If the entry has pages, add Prev/Next Page buttons
                if enc.active.has_pages:
                    hbox:
                        style "encyclopaedia_entry_change_entry_hbox"

                        textbutton _("Previous Page") xalign .02 action enc.PreviousPage() style "encyclopaedia_entry_change_entry_button"

                        # Flavour text to indicate which page out of the total is being viewed
                        text _("Page [enc.active.current_page.number] / [len(enc.active.pages)]") size 18 yalign 0.5

                        textbutton _("Next Page") xalign .98 action enc.NextPage() style "encyclopaedia_entry_change_entry_button"

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
                    textbutton _("Close Entry") id "close_entry_button" xalign .98 clicked enc.CloseActiveEntry() style "encyclopaedia_close_button"


screen inside_ul(element):
    if element.text:
        frame:
            style "html_ul"
            text "[element.text]" style element.style size 14

screen inside_ol(element):
    if element.text:
        frame:
            style "html_ol"
            text "[element.text]" style element.style size 14

screen code_block(element):
    frame:
        style "html_code_block"
        text "[element.text]" style "encyclopaedia_entry_text" size 14
