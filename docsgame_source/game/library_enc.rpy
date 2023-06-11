# Overlay screen with a button that takes the player to an Encyclopaedia.
screen enc_button():
    frame:
        background Transform(Solid('#000'), alpha=0.5)
        xfill True
        padding (8, 8, 8, 8)

        imagebutton:
            idle "images/enc_icon.png"
            hover Transform("images/enc_icon.png", matrixcolor=InvertMatrix(1.0))
            action ShowMenu(library_enc.list_screen, enc=library_enc)
            xalign 0.05
            yalign 0.05


# Shown as part of a callback when an entry is unlocked.
screen notify_entry_unlocked():
    text _("New Entry Unlocked") xalign 0.98 yalign 0.02

    timer 2.0 action Hide('notify_entry_unlocked')


init python:
    def notify_entry_unlocked(source):
        """This function is called when an entry is unlocked."""
        renpy.show_screen('notify_entry_unlocked')


label setup_enc:

    python:
        library_enc = Encyclopaedia(
            name="Wanderer in the Library",
            show_locked_buttons=True,
        )

        # Register a callback function.
        library_enc.on('entry_unlocked')(notify_entry_unlocked)

        # Use EncEntryTemplate to set reasonable defaults and reduce duplication
        LibraryEntry = EncEntryTemplate(parent=library_enc, locked=True)

        about_library = LibraryEntry(
            name=_('Library'),
            subject=_('Locations'),
            text=(
                "You find yourself sitting on a comfortable armchair. "
                "Around you, rows of books. "
                "You are in what appears to be a library, somehow."
            ),
            image=Transform('images/library.png', zoom=0.5),
        )

        about_library_2 = EncEntry(
            parent=about_library,
            name=_("Library"),
            subject=_('Locations'),
            text=(
                "As far as you can see, long, elegant curved columns rise "
                "several meters upwards. "
                "They bend at a slight angle and become arches along the ceiling."
            ),
            locked=True,
            image=Transform('images/library.png', zoom=0.5),
        )

        about_library_3 = EncEntry(
            parent=about_library,
            name=_("Library"),
            subject=_('Locations'),
            text=(
                "You attempt to look down a row of books, but become dizzy from the effort."
            ),
            locked=True,
            image=Transform('images/library.png', zoom=0.5),
        )

        about_garden = LibraryEntry(
            name=_('Garden'),
            subject=_('Locations'),
            text=[
                "You focus on the concept of outside.",
                (
                    "As you walk through rows of books, you notice their titles "
                    "have become nearly all related to gardening and camping."
                ),
                (
                    "You see something creating a gap between 2 rows. "
                    "A stone pillar, and on it you see a door. "
                    "The door is solid matte black with an ornate, silver door handle. "
                    "You touch the door with an open palm. It feels like a chilled slab of granite. "
                    "You grab the equally cold door handle and prepare for a struggle, but the door opens with ease. "
                    "Natural light bathes your face. "
                    "You step through and find yourself in an elegant garden. "
                )
            ],
            image=Transform('images/garden.png', zoom=0.5),
        )

        about_librarian = LibraryEntry(
            name=_('Librarian'),
            subject=_('People'),
            text=[
                "The person before you claims to be a librarian.",
                ("Surrounded by so many books, it does not seem too unreasonable a claim.")
            ],
        )

    return
