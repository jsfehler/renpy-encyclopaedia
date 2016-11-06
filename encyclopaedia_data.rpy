# In the following example, an encyclopaedia is created inside an "init python" block.
# This allows an encyclopaedia's content to be independent of the saved games. 
# ie: Whenever encyclopaedia content is unlocked, it's unlocked for all save games.
# If you want an encyclopaedia that is bound to a save game file, create the encyclopaedia in a "python" block inside the "start" label.
# Then, for the "locked" argument in each entry, don't use a persistent variable.    

init python:

    # Variables to hold the text.
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in nisl magna. Fusce nec bibendum magna, sed venenatis erat. Sed non dapibus augue, quis hendrerit diam. Quisque bibendum turpis vitae orci iaculis volutpat. Proin venenatis, nunc quis tempus convallis, lectus eros ultrices sem, eu condimentum tellus nisi sed magna. Curabitur laoreet posuere orci eu eleifend. Vivamus sed dui dignissim, egestas lorem eu, lobortis arcu. Duis venenatis sem eu ipsum condimentum adipiscing. Ut vel augue ut velit bibendum varius pharetra nec ligula. Duis eu sollicitudin mauris. Praesent vestibulum ligula vel ligula condimentum dignissim. Ut risus velit, laoreet sed pellentesque sed, suscipit in massa. Etiam posuere fringilla purus."
    cras = "Cras pretium, tellus ac tristique dapibus, mauris eros convallis libero, nec porta urna leo sed mi. Quisque non metus ac lacus sodales blandit. Maecenas dapibus justo vitae hendrerit placerat. Phasellus mollis sem nunc, sed porta ligula ullamcorper sit amet. Vivamus posuere vestibulum velit, nec facilisis metus hendrerit sit amet. Vivamus vulputate cursus massa sit amet sagittis. Donec ullamcorper arcu sit amet nibh elementum posuere. Suspendisse lectus ligula, luctus sit amet placerat et, molestie vel diam. Donec suscipit ut urna pulvinar molestie. Suspendisse suscipit placerat ligula, ac mattis neque malesuada ut. Cras aliquet malesuada mauris eu venenatis. Sed dapibus quis leo at ultricies. Integer laoreet elit semper ante hendrerit hendrerit. Ut eget nisl justo. Duis sit amet dolor lectus. Aenean aliquet porttitor pellentesque."
    infeu = "In feugiat ut magna vitae tincidunt. Suspendisse mi odio, tincidunt a ante in, consectetur iaculis lacus. Aenean non mi vitae risus congue bibendum ut id magna. Sed ornare sit amet nulla eu tempor. Sed aliquam nisi nisl, in auctor mauris convallis non. Suspendisse nec lacus tristique erat sodales auctor quis sed est. Nullam vitae feugiat dui. Maecenas tempor, urna quis ullamcorper accumsan, ligula leo tincidunt justo, sagittis vulputate nulla dui quis tellus. Ut felis lacus, tempus eget bibendum id, feugiat sit amet dolor. Proin cursus at risus hendrerit scelerisque. Sed posuere lorem non lacus aliquam, nec faucibus quam tempus. Praesent eu velit in magna bibendum interdum."
    morbi = "Morbi lobortis ipsum felis, eget rutrum nulla rhoncus et. Ut et interdum lorem. Quisque sed mi vitae enim pulvinar ultricies id id tellus. Nunc non lectus nibh. Pellentesque id dui elementum, lacinia velit a, luctus urna. Donec tempus augue et diam pretium commodo. Phasellus bibendum leo ut augue hendrerit sollicitudin. Quisque et tellus at tortor fringilla pellentesque."
    mauris = "Mauris et risus at elit pharetra gravida. Nulla in est magna. Integer in pulvinar mauris. Etiam diam felis, sollicitudin vel nisi ac, rutrum bibendum quam. Sed mattis sodales est, in ultricies felis commodo et. Cras tempor tortor at viverra auctor. Suspendisse a imperdiet lacus, non auctor enim. Vivamus vel aliquam ligula. Duis viverra volutpat metus, quis scelerisque nibh dictum in. Fusce imperdiet posuere quam quis ultricies. In hac habitasse platea dictumst. Cras dignissim felis nibh, in consectetur dolor luctus eu. Quisque adipiscing turpis massa, ut ultricies dolor aliquam eu. Maecenas ac libero porttitor, bibendum libero ac, dapibus enim."
    wine = "Wine, so good."
    wine2 = "More Wine"
    wine3 = "More Wine 3x" 
    
    # A list of strings can be used instead of a single string.
    # The default UI will show this as paragraphs.
    women = [
        "Who does not Love Wine Wife & Song will be a Fool for his Lifelong!",
        "Wine, women, and song is a hendiatris that endorses hedonistic lifestyles or behaviours. In modern times, it is usually seen in the form sex, drugs, and rock 'n' roll.",
    ]

    # Variables to hold the image paths. The path is relative to your game/ directory.
    en1_image = "enc_images/1266537434812.png"
    en2_image = "enc_images/1381014062018.jpg"
    en3_image = "enc_images/Rtx-011.jpg"
    en4_image = "enc_images/Xord_concept.jpg"
    en7_image = "enc_images/Thanatos_sprite.png"
    getting_started = "img/getting_started.png"

    # Define an encyclopaedia object.
    
    # If show_locked_buttons=False, it will not display locked entries on the list screen.
    # If True, locked entries will be displayed with "???" instead of their title.
    
    # If show_locked_entry=False, it will prevent the player from viewing the locked entry.
    # if True, locked entries can be viewed, but the title, text, and image will be replaced with "???".

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

    # Let's store the names of our subjects as variables. 
    # You can just use the strings when making the EncEntry, but doing it like this will help prevent typos,
    # and make it easier to change the subject title if you change your mind during development.  
    # Subjects are picked up and added when they're used in an entry, but can also be added independently.
    subject_lorem_ipsum = 'Lorem Ipsum'
    subject_virtues = 'Virtues'
    
    # Here we define each Encyclopaedia Entry
    # The arguments are: number, name, text, subject, status, locked, image
    # if save game independent, status should always be from the persistent.new_status or it won't save
    # if locked=False, entry will always be visible, even if new game hasn't been started
    en1 = EncEntry(
        encyclopaedia,
        1,
        "Lorem",
        lorem,
        subject_lorem_ipsum,
        viewed=persistent.new_status["new_00"],
        locked=False,
        image=en1_image
    )

    en2 = EncEntry(
        encyclopaedia,
        2,
        "Cras",
        cras,
        subject_lorem_ipsum,
        viewed=persistent.new_status["new_01"],
        locked=False,
        image=en2_image
    )

    en3 = EncEntry(
        encyclopaedia,
        3,
        "In",
        infeu,
        subject_lorem_ipsum,
        viewed=persistent.new_status["new_02"],
        locked=False,
        image=en3_image
    )

    en4 = EncEntry(
        encyclopaedia,
        4,
        "Morbi",
        morbi,
        subject_lorem_ipsum,
        viewed=persistent.new_status["new_03"],
        locked=persistent.en4_locked,
        image=en4_image,
        locked_image=None
    )

    en5 = EncEntry(
        encyclopaedia,
        5,
        "Mauris",
        mauris,
        subject_lorem_ipsum,
        viewed=persistent.new_status["new_04"],
        locked=False
    )

    en6 = EncEntry(
        encyclopaedia,
        6,
        "Wine",
        wine,
        subject_virtues,
        viewed=persistent.new_status["new_05"],
        locked=persistent.en6_locked
    )

    en7 = EncEntry(
        encyclopaedia,
        7,
        "Women",
        women,
        subject_virtues,
        viewed=persistent.new_status["new_06"],
        locked=persistent.en7_locked,
        image=en7_image,
        locked_image=None
    )

    ################
    # Documentation
    #

    # Basic Usage
    getting_started = EncEntry(
        encyclopaedia,
        8,
        "Getting Started",
        [
            "Inside an init python block, create a new Encyclopaedia object.",
        ],
        "Basic Usage",
        viewed=persistent.new_status["new_07"],
        locked=False,
        image=getting_started,
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
        image=en7_image,
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
        image=en7_image
    )

    locking_unlocking_entries = EncEntry(
        encyclopaedia,
        9,
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
        10,
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
        11,
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
        20,
        "Encyclopaedia",
        [
            "Encyclopaedias can take four optional arguments when being created:"
            " \n 1 - The default sorting mode. Default is by number."
            " \n 2 - If locked buttons should be displayed or not. Default is False."
            " \n 3 - If locked entries should be displayed or not. Default is False."
            " \n 4 - The screen to display individual entries on. Default is 'encyclopaedia_entry'."
        ],
        "In-Depth",
        viewed=False,
        locked=False
    )

    customizing_screens = EncEntry(
        encyclopaedia,
        11,
        "Customizing Screens",
        [""],
        "In-Depth",
    )

    translations = EncEntry(
        encyclopaedia,
        12,
        "Translations",
        [""],
        "In-Depth",
    )

    # Sorting
    # Filtering

    for x in range(13, 500):
        e = EncEntry(
            encyclopaedia,
            x,
            "Test Entry: " + str(x),
            "Test Entry",
            "Test Entries",
        )


    # en4 and en6 won't be viewed at the start because
    # they're locked by persistent data.
    # After they're unlocked, they'll be available whenever the game loads. 

    # When creating sub-entries, the main entry is considered page 1,
    # so always start at 2.
    en2_2 = EncEntry(
        en2,
        2,
        "Cras 2",
        "Cras 2",
        "Virtues",
        locked=False
    )

    en2_3 = EncEntry(
        en2,
        3,
        "Cras 3",
        "Cras 3",
        "Virtues",
        locked=persistent.en2_3_locked
    )

    en6_2 = EncEntry(
        en6,
        2,
        "Wine 2",
        wine2,
        "Virtues",
        locked=persistent.en6_2_locked
    )
    en6_3 = EncEntry(
        en6,
        3,
        "Wine 3",
        wine3,
        "Virtues",
        locked=persistent.en6_3_locked
    )
