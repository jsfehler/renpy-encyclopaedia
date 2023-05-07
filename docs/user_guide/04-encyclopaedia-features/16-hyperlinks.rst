Hyperlinks
==========

During your game, you might want to have some in-game text link directly to an EncEntry.
The `set_entry` hyperlink can be used to open the Encyclopaedia directly to a specific EncEntry.

Example:

.. code-block:: renpy

    init python:
      my_enc = Encyclopaedia(...)

      my_entry = EncEntry(...)


    label start:

        e "Lorem ipsum {a=set_entry:my_enc->entry_one}dolor sit{/a} amet"
