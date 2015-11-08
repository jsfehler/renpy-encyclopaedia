#Encyclopaedia Framework for Ren'Py
Ren'Py plugin for managing text entries. 
Useful for an encyclopaedia, bestiary, or similar system. 
The Encyclopaedia holds multiple EncEntries and offers different ways to sort
and display them.

##Features
- Sort entries by Number, Alphabetical, Reverse Alphabetical, Subject, or Unread status.
- Entries can have multiple sub-pages.
- Entries can be locked at the start of the game and then unlocked as players progress.
- Locked entries can be displayed with placeholders or outright hidden.
- Unlocks can be tied to save games or independent.
- Unread Entries can be tagged.
- Access can be from the main menu or during the game.

##Quick Start
Dump the contents of this repo into a new Ren'Py project, replacing the existing script.rpy, and run it.

###Basic Usage
    encyclopaedia = Encyclopaedia()
    encyclopaedia.add_subject("Lorem Ipsum")
    en1 = EncEntry(number=1, 
                   name="Lorem", 
                   text="Lorem", 
                   subject="Lorem Ipsum", 
                   status=persistent.new_dict["new_00"], 
                   locked=False, 
                   image=en1_image)
    
    encyclopaedia.add_entry(en1)
    

###Handling Translations:
    # Create a new French LabelController
    french_labels = LabelController()
    
    #Change the labels to french
    french_labels.unread_entry_label = 'Nouveau!'
    
    # Create an Encyclopaedia
    encyclopaedia = Encyclopaedia()
    
    If the game's language is French, use the French labels instead of English.
    if language == 'French':
        encyclopaedia.labels = french_labels