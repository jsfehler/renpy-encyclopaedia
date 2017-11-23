Getting Started
===============

Installation
------------

To add the Encyclopaedia to your game,

1. Download the latest release at https://github.com/jsfehler/renpy-encyclopaedia/releases
2. Place the Encyclopaedia files into your project's 'game' directory.

Creating an Encyclopaedia
-------------------------

Global vs Local
~~~~~~~~~~~~~~~

An Encyclopaedia can either be created in an `"init python:" <https://www.renpy.org/doc/html/python.html#init-python-statement>`_ block
or in a `"python" <https://www.renpy.org/doc/html/python.html#python-statement>`_ block inside the start label.

The difference is that the former is a global Encyclopaedia: Reading and unlocking entries at any point will affect the Encyclopaedia permanently.
The latter is local; the state of the Encyclopaedia will be different across every saved game.

Global Encyclopaedia's must use `persistent data <https://www.renpy.org/doc/html/persistent.html>`_ to save their state.


Creating the Encyclopaedia object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After deciding what type of Encyclopaedia you want, now you need to initialize one with the Encyclopaedia object.

This is the top-level container for all your entries.

Global:

.. code-block:: python

    init python:
        your_new_encyclopaedia = Encyclopaedia()

Local:

.. code-block:: python

    label start:
        python:
            your_new_encyclopaedia = Encyclopaedia()

Adding Entries
--------------

Once you have an Encyclopaedia, EncEntry objects need to be created.
These are where the information for each entry goes.
The minimum arguments to create an EncEntry are:

- parent: The container for the entry. Can be an Encyclopaedia or another EncEntry (for sub-pages)

- name: The name for the entry. Doesn't need to be unique.

- text: The text for the entry. Can be a string or list of strings.

.. code-block:: python

    about_zeus = EncEntry(
        parent=your_new_encyclopaedia,
        name="Zeus",
        text=[
            "Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus."
            " His name is cognate with the first element of his Roman equivalent Jupiter."
            " His mythologies and powers are similar, though not identical, to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin."
        ]
    )

