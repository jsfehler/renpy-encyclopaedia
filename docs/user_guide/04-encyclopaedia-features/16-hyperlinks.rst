Hyperlinks
==========

During your game, you might want to have some in-game text link directly to an EncEntry.
The `set_entry` hyperlink can be used to open the Encyclopaedia directly to a specific EncEntry.

Example:

.. code-block:: renpy

    init python:
        enc_enc = Encyclopaedia(...)

        dev_entry = EncEntry(...)


    label start:

        e "Want to learn how to build this {a=set_entry:enc_enc->dev_entry}documentation{/a} from source?"
