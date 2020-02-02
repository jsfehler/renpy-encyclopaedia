##############################################################################
# Encyclopaedia Button
# Contains a button to open the encyclopaedia at any time during the game
screen show_enc_button:
    textbutton "Open Encyclopaedia" xalign .98 yalign .02 action ShowMenu("encyclopaedia_list", encyclopaedia)

# The game starts here.
label start:

    # Display the Open Encyclopaedia button.
    show screen show_enc_button

    "Do you want to unlock an entry?"

    menu:
        "Yes":
            $ locked_entry.locked = False

        "No":
            "They weren't added."

    "Well done."

    return
