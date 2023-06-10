Screens
=======

The framework includes default `screens <https://www.renpy.org/doc/html/screens.html>`_
you can use to display the Encyclopaedia's data.

These screens can be skinned by modifying their styles or customized using Ren'Py Screen Language.
They can also be used as guides for creating completely new screens that use an Encyclopaedia.

They're located in `encyclopaedia/screens.rpy`.

encyclopaedia_list
------------------

This screen contains a list of entries in an Encyclopaedia.
It displays all the entries in a vertical list of textbuttons,
along with sorting and filtering options.

It takes one argument: The instance of the Encyclopaedia you want to display.

It uses `Textbutton <https://www.renpy.org/doc/html/screens.html#textbutton>`_ for links to each EncEntry.

encyclopaedia_list has 2 subscreens:

- `entry_button`: Decides the behaviour of the Textbutton to show for each EncEntry.

- `vertical_list`: Creates the vertical list of Textbuttons.

encyclopaedia_entry
-------------------

The default screen for showing the data in a single EncEntry.
It takes one argument: The Encyclopaedia you want to fetch entries from.

This screen should only be opened using the SetEntry Action.

Example:

.. code-block:: renpy

    init python:
        my_enc = Encyclopaedia(...)
        my_encentry = EncEntry(parent=my_enc, ...)

    screen my_screen:
        textbutton "Open My EncEntry" action my_enc.SetEntry(my_encentry)


This screen implements the PreviousEntry and NextEntry Actions to scroll between Entry objects.
It also uses the PreviousPage and NextPage Actions to scroll between pages in an Entry.
