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
    
    # A list of strings can be used instead of a single string. The default UI will show this as paragraphs.
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

    # Define an encyclopaedia object.
    
    # If showLockedButtons=False, it will not display locked entries on the list screen. 
    # If True, locked entries will be displayed with "???" instead of their title.
    
    # If showLockedEntry=False, it will prevent the player from viewing the locked entry.
    # if True, locked entries can be viewed, but the title, text, and image will be replaced with "???".
    encyclopaedia = Encyclopaedia(showLockedButtons=True, showLockedEntry=True) 
    
    # If the encyclopaedia is save game independent, run this function to generate the persistent status variables. 
    # If the encyclopaedia is unique for each save game, comment out or delete this.
    
    # entries_total is the total number of EncEntries the Encyclopaedia will hold.
    # master_key and name are what determines the name of the status variables and the name of each key.
    # only change master_key and name if you need multiple encyclopaedias in a game.
    encyclopaedia.setPersistentStatus(entries_total=7, master_key="new", name="new")
    
    # Add all the subjects the Encyclopaedia will have.
    encyclopaedia.addSubjects("Lorem Ipsum", "Virtues")
    # To do this one at a time, use addSubject() instead.
    
    # Here we define each Encyclopaedia Entry
    # The arguments are: number, name, text, subject, status, locked, image
    # if save game independent, status should always be from the persistent.new_dict or it won't save
    # if locked=False, entry will always be visible, even if new game hasn't been started
    en1 = EncEntry(0, "Lorem", lorem, "Lorem Ipsum", status=persistent.new_dict["new_00"], locked=False, image=en1_image)
    en2 = EncEntry(1, "Cras", cras, "Lorem Ipsum", status=persistent.new_dict["new_01"],  locked=False, image=en2_image)
    en3 = EncEntry(2, "In", infeu, "Lorem Ipsum", status=persistent.new_dict["new_02"], locked=False, image=en3_image)
    en4 = EncEntry(3, "Morbi", morbi, "Lorem Ipsum", status=persistent.new_dict["new_03"], locked=persistent.en4_locked, image=en4_image, locked_image=None)
    en5 = EncEntry(4, "Mauris", mauris, "Lorem Ipsum", status=persistent.new_dict["new_04"], locked=False)
    en6 = EncEntry(5, "Wine", wine, "Virtues", status=persistent.new_dict["new_05"], locked=persistent.en6_locked)
    en7 = EncEntry(6, "Women", women, "Virtues", status=persistent.new_dict["new_06"], locked=persistent.en7_locked, image=en7_image, locked_image=None)
  
    # Add all entries and sub-entries in an init block.
    encyclopaedia.addEntries(en1, en2, en3, en4, en5, en6, en7) 
    # To do this one at a time, use addEntry() instead
    # This auto-sorts when adding.
    
    # en4 and en6 won't be viewed at the start because they're locked by persistent data.
    # After they're unlocked, they'll be available whenever the game loads. 

    #When creating sub-entries, the main entry is considered page 1, always start at 2
    en2_2 = EncEntry(2, "Cras 2", "Cras 2", "Virtues", locked=False)
    en2_3 = EncEntry(3, "Cras 3", "Cras 3", "Virtues", locked=persistent.en2_3_locked)

    en6_2 = EncEntry(2, "Wine 2", wine2, "Virtues", locked=persistent.en6_2_locked)
    en6_3 = EncEntry(3, "Wine 3", wine3, "Virtues", locked=persistent.en6_3_locked)

    en2.addSubEntries(en2_2, en2_3)
    en6.addSubEntries(en6_2, en6_3)