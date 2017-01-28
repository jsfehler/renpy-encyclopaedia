##############################################################################
# Encyclopaedia Button
# Contains a button to open the encyclopaedia at any time during the game
screen show_enc_button:
    textbutton "Open Encyclopaedia" xalign .98 yalign .02 action ShowMenu("encyclopaedia_list", encyclopaedia)
 
# The game starts here.
label start:
 
    # Display the Open Encyclopaedia button.
    show screen show_enc_button   
  
    "Do you want to unlock a sub-entry?"

    # Unlocking an entry during the game requires the lock flag to be set to False, and then the encyclopaedia to be updated.
    menu:
        "Yes":
            $ persistent.lock_unlock_3 = False
            $ locking_unlocking_entries.unlock_sub_entry(locking_unlocking_entries_3)

        "No":
            "They weren't added." 

    "Excellent."

    return
