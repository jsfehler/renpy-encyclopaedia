screen enc_button():
    imagebutton:
        idle "images/enc_icon.png"
        action ShowMenu("encyclopaedia_list", enc=library_enc)
        xalign 0.05
        yalign 0.05

label setup_enc:

    python:
        library_enc = Encyclopaedia()

        # Use EncEntryTemplate to set reasonable defaults and reduce duplication
        LibraryEntry = EncEntryTemplate(parent=library_enc, locked=True)

        about_library = LibraryEntry(
            name=_('Library'),
            text="It appears to be a library.",
        )

        about_library_2 = EncEntry(
            parent=about_library,
            name=_("Library"),
            text="You are in a library.",
            locked=True,
        )

        about_librarian = LibraryEntry(
            name=_('Librarian'),
            text="It appears to be a librarian.",
        )

    return
