# Scenario:
#   Using the standard display, create an Encyclopaedia that displays entries
#   alphabetically with every entry nested under a letter of the alphabet

init -1 python:
    # Imports
    from encyclopaedia import Encyclopaedia
    from encyclopaedia import EncEntry
    from encyclopaedia import StatusFlagGenerator
    from encyclopaedia import ButtonModel

    # Create an Encyclopaedia object.
    # We'll call this one john_notes.
    john_notes = Encyclopaedia(
        show_locked_buttons=True,
        show_locked_entry=True,
        entry_screen="encyclopaedia_entry"
    )

    # Create a ButtonModel object and associate it with the Encyclopaedia
    # The button model is where we handle all the logic related to
    # displaying buttons
    button_model = ButtonModel(john_notes)