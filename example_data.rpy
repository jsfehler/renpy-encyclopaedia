################################################################################
# In the following example, an encyclopaedia is created inside an "init python" block.
# This allows an encyclopaedia's content to be independent of the saved games.
# ie: Whenever encyclopaedia content is unlocked, it's unlocked for all save games.
# If you want an encyclopaedia that is bound to a save game file, create the encyclopaedia in a "python" block inside the "start" label.
# Then, for the "locked" argument in each entry, don't use a persistent variable.
################################################################################

init python:
    # Variables to hold the image paths. The path is relative to your game/ directory.
    image_getting_started = "img/getting_started.png"
    image_translations = "img/translations.png"
    image_locked_image = "img/locked.png"

    # Define an encyclopaedia object.
    encyclopaedia = Encyclopaedia(
        show_locked_buttons=True,
        show_locked_entry=True,
        entry_screen="encyclopaedia_entry"
    )

    ################
    # Documentation
    ################

    ### Basic Usage ###
    getting_started = EncEntry(
        parent=encyclopaedia,
        name="Getting Started",
        text=[
            "Inside an init python block, create a new Encyclopaedia object."
            " This is the top-level container for all your entries.",
        ],
        subject="Basic Usage",
        viewed_persistent=True,
        locked=False,
        image=image_getting_started,
    )

    getting_started_1 = EncEntry(
        parent=getting_started,
        name="Getting Started",
        text=[
            "Once you have an Encyclopaedia, EncEntry objects can be created and placed inside the Encyclopaedia.",
            "Each EncEntry represents an individual entry in an encyclopaedia.",
            "The minimum arguments to create an EncEntry are:",
            "\n parent: The container for the entry. Can be an Encyclopaedia or another EncEntry (for sub-pages)",
            "\n name: The name for the entry. Doesn't need to be unique.",
            "\n text: The text for the entry. Can be a string or list of strings.",
        ],
        subject="Basic Usage",
        viewed=False,
        locked=False,
    )

    getting_started_2 = EncEntry(
        parent=getting_started,
        name="Getting Started",
        text=[
            "Once your Encyclopaedia is created and filled with EncEntries, you need to give players a way to access the encyclopaedia screens.",
            "You can add a button on the main menu, add a button in-game, or both, depending on your game.",
            "The action to use for the button is ShowMenu() with 2 arguments. The first must be the name of the screen, and the second the encyclopaedia object.",
            "The default screen included with the framework is encyclopaedia_list."
        ],
        subject="Basic Usage",
        viewed=False,
        locked=False,
    )

    locking_unlocking_entries = EncEntry(
        parent=encyclopaedia,
        name="Locking and Unlocking Entries",
        text=[
            "By default, all EncEntry objects are unlocked. They can be viewed by players at any time.",
            "However, when creating an EncEntry, the locked argument can be given with a variable as a flag, effectively hiding the entry until the condition is true.",
            "The entry will be locked until an the unlock_entry() function is called on the entry to unlock it."
        ],
        subject="Basic Usage",
        viewed_persistent=True
    )

    locking_unlocking_entries_1 = EncEntry(
        parent=locking_unlocking_entries,
        name="Locking and Unlocking Entries",
        text=[
            "If the encyclopaedia is tied to a save game, setting an entry as locked is as easy as giving the locked argument a boolean. Unlocking only requires calling unlock_entry().",
            "However, if the encyclopaedia's state must persist outside of an individual save game, Ren'Py persistent data must be given as an argument, and it must be explicitly set to unlock it.",
            "The framework includes a function to create the necessary persistent variables for you. This is covered in the In-Depth section.",
            "The following page in this entry can be unlocked by playing through the game."
        ],
        subject="Basic Usage"
    )

    locking_unlocking_entries_3 = EncEntry(
        parent=locking_unlocking_entries,
        name="Locking and Unlocking Entries",
        text=["This entry was unlocked while playing."],
        subject="Basic Usage",
        locked=persistent.lock_unlock_3
    )

    adding_pages = EncEntry(
        parent=encyclopaedia,
        name="Adding Sub-Pages",
        text=[
            "Just like an Encyclopaedia holds EncEntry objects, each EncEntry can hold other EncEntry. This allows entries to have multiple pages.",
            "EncEntry that are used as sub-pages are created the same way as other EncEntry, but instead of providing an Encyclopaedia as the parent, an EncEntry is given.",
        ],
        subject="Basic Usage",
        viewed_persistent=True
    )

    adding_pages_1 = EncEntry(
        parent=adding_pages,
        name="Adding Sub-Pages",
        text=[
            "When adding sub-pages, the parent EncEntry is considered the first page in the entry. Added sub-pages are numbered starting from 2."
        ],
        subject="Basic Usage",
    )

    placeholders = EncEntry(
        parent=encyclopaedia,
        name="Placeholder Data",
        text=[
            "Every EncEntry can be given placeholders for the name, text, and image.",
            "This allows you to display a locked entry without revealing what the content of the entry is until it has been unlocked.",
            "If no specific placeholders are provided, a default placeholder is used for the name and text. The default placeholder image will be a dark tinted version of the normal image.",
            "An example of this can be seen in the next entry.",
        ],
        subject="Basic Usage",
        viewed_persistent=True
    )

    placeholders_locked = EncEntry(
        parent=encyclopaedia,
        name="Placeholder Data Example",
        text=["This entry was unlocked."],
        subject="Basic Usage",
        locked=True,
        viewed_persistent=True,
        image=image_locked_image
    )

    writing_text = EncEntry(
        parent=encyclopaedia,
        name="Writing Text",
        text=[
            "Text in an EncEntry is stored in a list."
            " You can use either a single string or a list of strings when creating the EncEntry."
            " If a single string is given it will simply be placed inside a list as the first and only item.",
            "On the default screen provided for displaying an EncEntry, each list item is treated as a line break."
            "\n",
            "Remember, there's a difference between how text looks in your script file and how it looks on screen. Take the following letters:",
            "X"
            "Y"
            "Z",

            "They're on three separate lines in the script, but will be displayed as one line since there's no comma separating them. They count as one list item.",
        ],
        subject="Basic Usage",
        viewed_persistent=True,
        locked=False,
    )

    ### In-Depth ###
    # Encyclopaedia
    # EncEntry
    # Actions

    encyclopaedia_options = EncEntry(
        parent=encyclopaedia,
        name="Encyclopaedia Object",
        text=[
            "Encyclopaedias can take four optional arguments when being created:"
            " \n 1 - The default sorting mode. If not set, will use sorting by number."
            " \n 2 - If locked buttons should be displayed or not. Default is False. Locked buttons will use placeholder values."
            " \n 3 - If locked entries should be displayed or not. Default is False. Locked entries will use placeholder values."
            " \n 4 - The screen to display individual entries on. Default is 'encyclopaedia_entry'.",

            "The following attributes are available:",
            "all_entries (list): All entries, regardless of status.",
            "unlocked_entries (list): Only unlocked entries.",
            "filtered_entries (list): Entries that match a subject filter.",
            "filtering (bool|str): The subject that's being used as a filter.",
            "size_all (int): Length of all_entries.",
            "size_unlocked (int): Length of unlocked_entries.",
            "reverse_sorting (bool): Should sorting occur in reverse or not.",
            "nest_alphabetical_sort (bool): Should alphabetical sorting display each letter as a subject.",
            "current_position (int): Index for the current entry open.",
            "sub_current_position (int): Index for the current sub-entry open. Starts at 1.",
            "labels (Labels): The current label controller.",
            "subjects (list): Collection of every subject.",
            "active (EncEntry): The currently open entry.",
            "locked_at_bottom (bool): If locked entries should appear at the bottom of the entry list or not."
        ],
        subject="In-Depth",
        viewed_persistent=True,
        locked=False
    )

    encentry_options = EncEntry(
        parent=encyclopaedia,
        name="EncEntry Object",
        text=[
            "EncEntry can take the following arguments when being created:",
                "parent (Encyclopaedia|EncEntry): The container for the EncEntry. Either an Encyclopaedia or another EncEntry.",
                "number (int): The number for the entry. If this is not set then it will be given a number automatically.",
                "name (str): The name that will be displayed for the entry's button and labels.",
                "text (str|list): The text that will be displayed when the entry is viewed",
                "subject (str): The subject to associate the entry with. Used for sorting and filtering.",
                "viewed (bool): Determines if the entry has been seen or not. This should only be set if the Encyclopaedia is save-game independent.",
                "locked (bool): Determines if the entry can be viewed or not. Defaults to False.",
                "image (str): The image displayed with the Entry text. Default is None.",
                "locked_name (str): Placeholder text for the name. Shown when the entry is locked.",
                "locked_text (str): Placeholder text for the text. Shown when the entry is locked.",
                "locked_image (str): Placeholder text for the image. Shown when the entry is locked.",
                "locked_image_tint (tuple): If no specific locked image is provided, a tinted version of the image will be used. The amount of tinting can be set with RGB values in a tuple.",
        ],
        subject="In-Depth",
        viewed_persistent=True,
        locked=False
    )

    customizing_screens = EncEntry(
        parent=encyclopaedia,
        name="Customizing Screens",
        text=[
            "The following screens are provided in the framework:",
            "encyclopaedia_list - Displays all the buttons used to visit entries, along with sorting and filtering options. It takes one argument: The Encyclopaedia you want to display on it.",
            "encyclopaedia_entry - Displays one single entry. It takes one argument: The Encyclopaedia you want fetch entries from.",
            "\n Both these screens can be skinned by modifying their styles, or can be customized entirely using Ren'Py Screen Language."
            "If your game has multiple Encyclopaedias, they can all use the same screens, if that's visually appropriate.",
            "You can also duplicate and modify these screens as much as desired, creating separate ones for each Encyclopaedia."
        ],
        subject="In-Depth",
        viewed_persistent=True
    )

    translations = EncEntry(
        parent=encyclopaedia,
        name="Translations",
        text=[
            "Translating the labels used by an Encyclopaedia can be done through the Labels object.",
            "Every Encyclopaedia is created with a default one that can be replaced.",
            "The attributes in the Labels object are used on the Encyclopaedia screens."

            "The following attributes are available:",
            "percentage_label (str): Placed next to the percentage unlocked number",
            "page_label (str): Placed before the entry page displayed",
            "page_separator_label (str): Placed in-between the current page number and the total page number",

            "sort_number_label (str): Label for Number Sorting",
            "sort_alphabetical_label (str): Label for Alphabetical sorting",
            "sort_reverse_alphabetical_label (str): Label for Reverse Alphabetical sorting",
            "sort_subject_label (str): Label for Subject sorting",
            "sort_unread_label (str): Label for Unread sorting",

            "unread_entry_label (str): Default for the tag next to unread entries",
            'locked_entry_label (str): Default for a "Locked Entry" button',

        ],
        subject="In-Depth",
        viewed_persistent=True,
        image=image_translations
    )

    numbering = EncEntry(
        parent=encyclopaedia,
        name="Manually Numbering Entries",
        text = [
            "When creating an entry, the 'number' argument can be used to specify what number the entry will have."
            " If it's not provided then the entry will be automatically assigned the next available number.",
            "Numbered entries must be defined before non-numbered entries."
        ],
        subject="In-Depth",
        viewed_persistent=True
    )

    # Sorting
    # Filtering
