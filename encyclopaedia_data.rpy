# In the following example, an encyclopaedia is created inside an "init python" block.
# This allows an encyclopaedia's content to be independent of the saved games. 
# ie: Whenever encyclopaedia content is unlocked, it's unlocked for all save games.
# If you want an encyclopaedia that is bound to a save game file, create the encyclopaedia in a "python" block inside the "start" label.
# Then, for the "locked" argument in each entry, don't use a persistent variable.    

init python:


    # Variables to hold the image paths. The path is relative to your game/ directory.
    image_getting_started = "img/getting_started.png"
    image_translations = "img/translations.png"

    # Define an encyclopaedia object.
    encyclopaedia = Encyclopaedia(
        sorting_mode = Encyclopaedia.SORT_NUMBER,
        show_locked_buttons=True,
        show_locked_entry=True,
        entry_screen="encyclopaedia_entry"
    )

    # If the encyclopaedia is save game independent, run this function to generate the persistent status variables. 
    # If the encyclopaedia is unique for each save game, comment out or delete this.
    
    # entries_total is the total number of EncEntries the Encyclopaedia will hold.
    # master_key and name are what determines the name of the status variables and the name of each key.
    # only change master_key and name if you need multiple encyclopaedias in a game.
    persistent_status_flags(
        total=8,
        master_key="new",
        status_name="new_status"
    )

    ################
    # Documentation
    ################

    # Basic Usage
    getting_started = EncEntry(
        encyclopaedia,
        1,
        "Getting Started",
        [
            "Inside an init python block, create a new Encyclopaedia object.",
        ],
        "Basic Usage",
        viewed=persistent.new_status["new_01"],
        locked=False,
        image=image_getting_started,
    )

    getting_started_1 = EncEntry(
        getting_started,
        2,
        "Getting Started",
        [
            "Once you have an Encyclopaedia, EncEntry objects can be created and placed inside the Encyclopaedia.",
            "Each EncEntry is an individual entry in an encyclopaedia.",
            "The minimum arguments to create an EncEntry are:",
            "\n parent: The container for the entry. Can be an Encyclopaedia or another EncEntry (for sub-pages)",
            "\n number: The number for the entry. Must be unique.",
            "\n name: A name for the entry. Doesn't need to be unique.",
            "\n text: The text for the entry. Can be a string or list of strings."
        ],
        "Basic Usage",
        viewed=False,
        locked=False,
    )

    getting_started_2 = EncEntry(
        getting_started,
        3,
        "Getting Started",
        [
            "Once your Encyclopaedia is created and filled with EncEntries, you need to give players a way to access the encyclopaedia screens.",
            "You can add a button on the main menu, add a button in-game, or both, depending on your game.",
            "The default screen included with the framework is encyclopaedia_list. It takes one argument: the encyclopaedia you want to show on it."
        ],
        "Basic Usage",
        viewed=False,
        locked=False,
    )

    locking_unlocking_entries = EncEntry(
        encyclopaedia,
        2,
        "Locking and Unlocking Entries",
        [
            "By default, all EncEntry objects are unlocked. They can be viewed by players at any time.",
            "However, when creating an EncEntry, the locked argument can be given with a variable as a flag, effectively hiding the entry until the condition is true.",
            "The entry will be locked until an the unlock_entry() function is called on the entry to unlock it.",
        ],
        "Basic Usage"
    )

    locking_unlocking_entries_1 = EncEntry(
        locking_unlocking_entries,
        2,
        "Locking and Unlocking Entries",
        [
            "If the encyclopaedia is tied to a save game, setting an entry as locked is as easy as giving the locked argument a boolean. Unlocking only requires calling unlock_entry().",
            "However, if the encyclopaedia's state must persist outside of an individual save game, Ren'Py persistent data must be given as an argument, and it must be explicitly set to unlock it.",
            "The framework includes a function to create the necessary persistent variables for you. This is convered in the In-Depth section."
        ],
        "Basic Usage"
    )


    adding_pages = EncEntry(
        encyclopaedia,
        3,
        "Adding Sub-Pages",
        [
            "Just like an Encyclopaedia holds EncEntry objects, each EncEntry can hold other EncEntry. This allows entries to have multiple pages.",
            "EncEntry that are used as sub-pages are created the same way as other EncEntry, but instead of providing an Encyclopaedia as the parent, an EncEntry is given.",
        ],
        "Basic Usage",
    )

    adding_pages_1 = EncEntry(
        adding_pages,
        2,
        "Adding Sub-Pages",
        [
            "When adding sub-pages, the parent EncEntry is considered the first page, so the number argument for sub-pages must start at 2."
        ],
        "Basic Usage",
    )

    placeholders = EncEntry(
        encyclopaedia,
        4,
        "Placeholders",
        [""],
        "Basic Usage"
    )

    # In-Depth
    # Encyclopaedia
    # EncEntry
    # Actions

    encyclopaedia_options = EncEntry(
        encyclopaedia,
        5,
        "Encyclopaedia",
        [
            "Encyclopaedias can take four optional arguments when being created:"
            " \n 1 - The default sorting mode. If not set, will be by number."
            " \n 2 - If locked buttons should be displayed or not. Default is False. Locked buttons will use placeholder values."
            " \n 3 - If locked entries should be displayed or not. Default is False. Locked entries will use placeholder values."
            " \n 4 - The screen to display individual entries on. Default is 'encyclopaedia_entry'."
        ],
        "In-Depth",
        viewed=False,
        locked=False
    )

    customizing_screens = EncEntry(
        encyclopaedia,
        6,
        "Customizing Screens",
        [""],
        "In-Depth",
    )

    translations = EncEntry(
        encyclopaedia,
        7,
        "Translations",
        [
            "Translating the labels used by an Encyclopaedia can be done through the LabelController object.",
            "Every Encyclopaedia is created with a default one that can be replaced.",
        ],
        "In-Depth",
        image=image_translations
    )

    # Sorting
    # Filtering

    # Stress testing
    #for x in range(25, 30):
    #    e = EncEntry(
    #        encyclopaedia,
    #        x,
    #        "Test Entry: " + str(x),
    #        "Test Entry",
    #        "Test Entries",
    #    )


    # When creating sub-entries, the main entry is considered page 1,
    # so always start at 2.

    locking_unlocking_entries_3 = EncEntry(
        locking_unlocking_entries,
        3,
        "Locking and Unlocking Entries",
        [
            "This entry was unlocked while playing."
        ],
        "Basic Usage",
        locked = persistent.lock_unlock_3
    )
