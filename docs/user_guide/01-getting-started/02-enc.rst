Create an Encyclopaedia
=======================

Fundamentally, an Encyclopaedia is built using two python classes:

    - `Encyclopaedia()`: The top level container.
    - `EncEntry()`: A container for a single encyclopaedia entry.

Encyclopaedia()
---------------

After deciding what type of Encyclopaedia you want, now you need to create one with the Encyclopaedia object.

This is the top-level container for all your entries.

.. code-block:: renpy

    init python:
        your_new_encyclopaedia = Encyclopaedia()

EncEntry
--------

Once you have an Encyclopaedia, EncEntry objects need to be created.
These are where the information for each entry goes.
The minimum arguments to create an EncEntry are:

- parent: The container for the entry. Can be an Encyclopaedia or another EncEntry (for sub-pages)

- name: The name for the entry. Doesn't need to be unique.

- text: The text for the entry. Can be a string or list of strings.

.. code-block:: renpy

    init python:
        your_new_encyclopaedia = Encyclopaedia()

        about_zeus = EncEntry(
            parent=your_new_encyclopaedia,
            name="Zeus",
            text=[
                "Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus."
                " His name is cognate with the first element of his Roman equivalent Jupiter."
                " His mythologies and powers are similar, though not identical, to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin."
            ]
        )
