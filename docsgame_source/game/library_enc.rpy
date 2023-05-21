screen enc_button():
    imagebutton:
        idle "images/enc_icon.png"
        action ShowMenu("encyclopaedia_list", enc=library_enc)
        xalign 0.05
        yalign 0.05

label setup_enc:

    python:
        library_enc = Encyclopaedia(
            name="Wanderer in the Library",
        )

        # Use EncEntryTemplate to set reasonable defaults and reduce duplication
        LibraryEntry = EncEntryTemplate(parent=library_enc, locked=True)

        about_library = LibraryEntry(
            name=_('Library'),
            text=(
                "You find yourself sitting on a comfortable armchair."
                "Around you, rows of books."
                "You are in what appears to be a library, somehow."
            ),
        )

        about_library_2 = EncEntry(
            parent=about_library,
            name=_("Library"),
            text=(
                "As far as you can see, long, elegant curved columns rise "
                "several meters upwards."
                "They bend at a slight angle and become arches along the ceiling."
            ),
            locked=True,
        )

        about_library_3 = EncEntry(
            parent=about_library,
            name=_("Library"),
            text=(
                "You attempt to look down a row of books, but become dizzy from the effort."
            ),
            locked=True,
        )

        about_librarian = LibraryEntry(
            name=_('Librarian'),
            text="It appears to be a librarian.",
        )

    return
