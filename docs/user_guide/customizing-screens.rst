Customizing Screens
===================

The following screens are provided in the framework and are found inside encyclopaedia_screens.rpy:

- encyclopaedia_list

- encyclopaedia_entry

Both these screens can be skinned by modifying their styles or using Ren'Py Screen Language.

They can also be used as guides for creating completely customized screens.
The screens an Encyclopaedia uses can be changed, making the use of these default screens completely optional.

encyclopaedia_list
------------------

This is the default screen shown when the Encyclopaedia is opened.
It displays all the buttons used to visit entries in a vertical list, along with sorting and filtering options.
It takes one argument: The Encyclopaedia you want to display.

It uses Textbuttons for links to each EncEntry.

encyclopaedia_list has 2 subscreens:

- entry_button: Decides which Textbutton to show for each EncEntry.

- vertical_list: Creates a vertical list of Textbuttons.

encyclopaedia_entry
-------------------

The default screen for showing the data in a single EncEntry.
It takes one argument: The Encyclopaedia you want to fetch entries from.

This screen should only be opened using the SetEntry Action.
When swapping the data of one entry for another, the PreviousEntry or NextEntry Actions should be used.
When swapping the data of one page for another, the PreviousPage or NextPage Actions should be used.
