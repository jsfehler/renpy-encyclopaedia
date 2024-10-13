Create an Encyclopaedia
=======================

Fundamentally, an Encyclopaedia's data is built using the following python classes:

- `Encyclopaedia()`: Top level container.
- `Book()`: Container for multiple entries.
- `EncEntry()`: Container for a single encyclopaedia entry.

A default GUI to display and interact with an Encyclopaedia is included with the framework.
This GUI can be skinned using Ren'Py's style system or completely replaced with your own.

Encyclopaedia
-------------

`Encyclopaedia` is a container to manage your entries. It handles:
    - The sorting and filtering of all your entries.
    - Which screens are used to display your Encyclopaedia.
    - Actions to interact with your Encyclopaedia from the GUI.

.. code-block:: renpy

    init python:
        greek_mythology = Encyclopaedia(name="Greek Mythology")


EncEntry
--------

`EncEntry` are where the information for each entry goes.

The minimum arguments to create an EncEntry are:

- parent: The container for the entry. Can be an Encyclopaedia, a Book, or another EncEntry.

- name: The name for the entry. This does not need to be unique.

- text: The text for the entry. Can be a string or list of strings.

.. code-block:: renpy

    init python:
        greek_mythology = Encyclopaedia()

        about_zeus = EncEntry(
            parent=greek_mythology,
            name="Zeus",
            subject="Gods",
            text=enc_utils.text_block("""\
                Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus.
                His name is cognate with the first element of his Roman equivalent Jupiter.
                His mythologies and powers are similar, though not identical,
                to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin.
            """)
        )

Book
----

Like Encyclopaedia, `Book` is a container, except that it goes inside an Encyclopaedia.
You can place entries inside a Book and place the Book inside your Encyclopaedia.

Using a Book is optional.
It's useful when multiple EncEntry have a close relationship and you want
them to be grouped and paginated together.

For example, in an Encyclopaedia about Greek Mythology,
instead of a separate item in your Encyclopaedia for each
entry about Zeus, you can place all the entries related to him inside a
Book:

.. code-block:: renpy

    init python:
        greek_mythology = Encyclopaedia(name="Greek Mythology")

        zeus = Book(
            parent=greek_mythology,
            title="Zeus",
            subject="Gods",
        )

        zeus_summary = EncEntry(
            parent=zeus,
            number=0,
            name="Summary",
            text=enc_utils.text_block("""\
                Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus.
                His name is cognate with the first element of his Roman equivalent Jupiter.
                His mythologies and powers are similar, though not identical,
                to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin.
            """)
        )
        zeus_marriage = EncEntry(
            parent=zeus,
            number=1,
            name="Marriage to Hera",
            text=enc_utils.text_block("""\
              While Hera is Zeus's seventh wife in Hesiod's version,
              in other accounts she is his first and only wife.
              In the Theogony, the couple has three children, Ares, Hebe, and Eileithyia.
              While Hesiod states that Hera produces Hephaestus on her own after Athena is born from Zeus's head,
              other versions, including Homer, have Hephaestus as a child of Zeus and Hera as well.
            """)
        )

With this configuration `zeus_summary` and `zeus_marriage` would not appear
as separate entries in the Encyclopaedia. They will not be sorted or filtered.
They will instead become pages in the `zeus` Book. That Book is what
the Encyclopaedia will use for sorting and filtering.
