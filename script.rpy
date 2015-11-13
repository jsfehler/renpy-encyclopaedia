init -1 python:
    # Encyclopaedia needs to be imported before it can be used
    from encyclopaedia import Encyclopaedia
    from encyclopaedia import EncEntry
    from encyclopaedia import StatusFlagGenerator
    from encyclopaedia import ButtonModel

##############################################################################
# Encyclopaedia Button
# Contains a button to open the encyclopaedia at any time during the game
screen show_enc_button:
    textbutton "Open Encyclopaedia" xalign .98 yalign .02 action ShowMenu("encyclopaedia_list")
 
# The game starts here.
label start:
 
    # Display the Open Encyclopaedia button.
    show screen show_enc_button   
  
    "Do you want to add entries 4 and 6?" 

    # Unlocking an entry during the game requires the lock flag to be set to False, and then the encyclopaedia to be updated.
    menu:
        "Yes":
            $ persistent.en6_locked = False
            $ encyclopaedia.unlock_entry(en6, persistent.en6_locked)
   
            $ persistent.en4_locked = False  
            $ encyclopaedia.unlock_entry(en4, persistent.en4_locked)
            "Ok, they're in. How about the sub-entries?" 
   
            menu:
                "Add Sub-Entry 6-2 and 6-3":
                    $ persistent.en6_2_locked = False   
                    $ en6.unlock_sub_entry(en6_2, persistent.en6_2_locked)
                    $ persistent.en6_3_locked = False  
                    $ en6.unlock_sub_entry(en6_3, persistent.en6_3_locked)

                "Add Sub-Entry 2-3":
                    $ persistent.en2_3_locked = False   
                    $ en2.unlock_sub_entry(en2_3, persistent.en2_3_locked)
   
                "Don't Add Sub-Entry":
                    "Ok"  
   
        "No":
            "They weren't added." 
   
    "How about entry 7?"
    menu:
        "Yes":
            $ persistent.en7_locked = False  
            $ encyclopaedia.unlock_entry(en7, persistent.en7_locked)
            "Done."
        "No":
            "How was it?"
            
    return