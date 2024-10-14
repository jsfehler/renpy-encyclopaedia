default l_name = '???'
define l = Character('l_name', dynamic=True, who_color='#008080')

image bg library = 'images/library.png'
image bg garden = 'images/garden.png'


label start:

    call setup_enc

    "..."

    l "Hmm..."

    menu:
        "Hello?":
            l "Oh, you can percieve me?"
            l "Curious."
            l "I wouldn't have thought we could interact in a pseudo-four dimensional interface."

        "What is this?":
            l "How strange."
            l "Are you..."
            l "You're approaching from a pseudo-four dimensional interface, aren't you?"

    l "Here, I'll make this place comprehensible to you."

    show bg library
    with fade

    l "That should do it."

    show screen enc_button

    $ library_book.locked = False
    $ about_library.locked = False

    l "Welcome to my {a=set_entry:library_enc->about_library}Library{/a}."

    l "Is there any knowledge you seek?"

    jump questions


label questions:

    menu:
        "Who are you?":
            l "A Librarian."

            $ l_name = _("Librarian")

            $ about_librarian.locked = False

        "Are we in a library?":
            l "Yes, that would be the most appropriate word."

            $ about_library_2.locked = False

        "How big is this place?" if not about_library_2.locked:
            l "Infinite, technically speaking."
            l "It's not something you can perceive."
            l "However I assure you, becoming lost is impossible."

            $ about_library_3.locked = False

        "Getting lost is impossible?" if not about_library_3.locked:
            l "Simply focus on returning to this place."
            l "You will find your way back."
            l "Likewise, focus on anything else to find your way there."

            $ about_garden.locked = False

        "How do I get out?" if not about_library_3.locked:
            l "The way you came in, I would assume."

            $ about_library_2.locked = False

    jump questions
