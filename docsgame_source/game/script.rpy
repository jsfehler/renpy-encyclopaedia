default l_name = '???'
define l = Character('l_name', dynamic=True, who_color='#008080')


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

    with fade

    l "That should do it."

    show screen enc_button

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

    jump questions
