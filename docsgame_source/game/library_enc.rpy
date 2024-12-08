# Overlay screen with a button that takes the player to an Encyclopaedia.
screen enc_button():
    frame:
        background Transform(Solid('#000'), alpha=0.5)
        xfill True
        padding (8, 8, 8, 8)

        hbox:
            spacing 16

            imagebutton:
                idle "images/enc_icon.png"
                hover Transform("images/enc_icon.png", matrixcolor=InvertMatrix(1.0))
                action ShowMenu(library_enc.list_screen, enc=library_enc)
                xalign 0.05
                yalign 0.05


            imagebutton:
                idle "images/ach_icon.png"
                hover Transform("images/ach_icon.png", matrixcolor=InvertMatrix(1.0))
                action ShowMenu(library_enc.list_screen, enc=library_ach)
                xalign 0.05
                yalign 0.05


# Shown as part of a callback when an entry is unlocked.
screen notify_entry_unlocked():
    text _("New Entry Unlocked") xalign 0.98 yalign 0.02

    timer 2.0 action Hide('notify_entry_unlocked')


init python:
    achievement.register("ACH_01")

    def notify_entry_unlocked(source):
        """This function is called when an entry is unlocked."""
        renpy.show_screen('notify_entry_unlocked')


    def unlock_ach(source):
        achievement.grant("ACH_01")


label setup_enc:
    python:
        library_enc = Encyclopaedia(
            name="Wanderer in the Library",
            show_locked_buttons=True,
        )

        # Register a callback function.
        library_enc.on('entry_unlocked')(notify_entry_unlocked)

        library_book = Book(parent=library_enc, title=_('Library'), subject=_('Locations'), locked=True)

        # Use EncEntryTemplate to set reasonable defaults and reduce duplication
        LibraryEntry = EncEntryTemplate(parent=library_enc, locked=True)

        about_library = EncEntry(
            parent=library_book,
            number=0,
            name=_('Library'),
            text=enc_utils.text_block("""\
            You find yourself sitting on a blue leather armchair.
            You sink into the comfort of the seat and look around.
            In front of you, a small coffee table.
            Around the coffee table there are more armchairs and a small sofa.
            A single book sits atop the table. You pick it up and scan the cover:
            "Names: Mythology & Narrative"

            You flip through the book. It seems to be a record of names and
            people with those names. Each person's record includes a set of
            detailed illustrations. You return the book to the table.

            Surrounding you is a circular shelf of books, at least a meter
            in height. There are gaps at each cardinal direction.

            You stand up and look around, then quickly sit down again.
            All you can see are rows of bookshelves packed with books.
            You are, somehow, sitting in what appears to be a small section of a massive library.
            """),
            locked=True,
            image=Transform('images/library.png', zoom=0.5),
        )

        about_library_2 = EncEntry(
            parent=library_book,
            number=1,
            name=_("Library"),
            text=(
                "As far as you can see, long, elegant curved columns rise "
                "several meters upwards. "
                "They bend at a slight angle and become arches along the ceiling."
            ),
            locked=True,
            image=Transform('images/library.png', zoom=0.5),
        )

        about_library_3 = EncEntry(
            parent=library_book,
            number=2,
            name=_("Library"),
            text=(
                "You attempt to look down a row of books, but become dizzy from the effort."
            ),
            locked=True,
            image=Transform('images/library.png', zoom=0.5),
        )

        garden_book = Book(parent=library_enc, title=_('Garden'), subject=_('Locations'), locked=True)

        about_garden = EncEntry(
            parent=garden_book,
            number=0,
            name=_('Garden'),
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

        # Grant an achievement when the entry is viewed.
        about_garden.on("viewed")(unlock_ach)

        about_garden_2 = EncEntry(
            parent=garden_book,
            number=1,
            name=_('Garden'),
            text=[
                "There is a peculiar calm to this garden.",
                (
                    "Rays of light shine through the canopy of trees, but you cannot quite make out the sky. "
                    "Paths are laid out in white stone, twisting around small ponds and leading towards a stone gazebo."
                ),
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

        library_ach = Encyclopaedia(
            name="Achievements",
            show_locked_buttons=True,
        )

        AchievementEncEntry(
            achievement="ACH_01",
            parent=library_ach,
            name="Garden Wanderer",
            subject="Achievements",
            text="You entered the Garden.",
        )

    return
