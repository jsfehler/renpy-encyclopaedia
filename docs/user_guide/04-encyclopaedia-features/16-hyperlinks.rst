.. _hyperlinks:

Hyperlinks
==========

You can have in-game text open an entry using Ren'Py's
`text anchors <https://www.renpy.org/doc/html/text.html#text-tag-a>`_.
The `set_entry` function will open an Encyclopaedia directly to a specific entry.
It takes 2 to 3 arguments, separated by `->`: The encyclopaedia variable name,
the entry variable name, and optionally the page number, if the entry is a Book.

Example:

.. code-block:: renpy

    init python:
        enc_enc = Encyclopaedia(...)

        dev_entry = EncEntry(...)


    label start:

        "Want to learn how to build this {a=set_entry:enc_enc->dev_entry}documentation{/a} from source?"
