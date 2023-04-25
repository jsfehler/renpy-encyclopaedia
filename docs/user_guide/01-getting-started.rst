Getting Started
===============

Installation
------------

To add the Encyclopaedia to your game:

1. Download the latest release at https://github.com/jsfehler/renpy-encyclopaedia/releases
2. Place `enc.rpy` and `encyclopaedia_screens.rpy` into your project's `game` directory.

Creating an Encyclopaedia
-------------------------

Global vs Local
~~~~~~~~~~~~~~~

An Encyclopaedia can either be created in an `"init python:" <https://www.renpy.org/doc/html/python.html#init-python-statement>`_ block
or in a `"python" <https://www.renpy.org/doc/html/python.html#python-statement>`_ block inside a label (usually the start label).

The difference is that the former is a global Encyclopaedia. It's initialized when the application is opened and can be accessed even if the player hasn't started a new game yet.
(ie: From the main menu). Since it runs outside of the normal game flow, global Encyclopaedias must use `persistent data <https://www.renpy.org/doc/html/persistent.html>`_ to save their state.
As a result, a global Encyclopaedia's state will not be bound to any particular save game.


The latter is local; the state of the Encyclopaedia will be different across every saved game. The state of the Encyclopaedia is saved when the player saves their game.
A local Encyclopaedia can only be accessed from within a new game. It should never be accessed from the main menu.

Creating the Encyclopaedia object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After deciding what type of Encyclopaedia you want, now you need to create one with the Encyclopaedia object.

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

Persistent Entries
~~~~~~~~~~~~~~~~~~

If you want an entry's viewed status to be persistent (ie: not tied to a particular save game), you must provide the viewed_persistent argument.

.. code-block:: python

    about_zeus = EncEntry(
        parent=your_new_encyclopaedia,
        name="Zeus",
        text=[
            "Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus."
            " His name is cognate with the first element of his Roman equivalent Jupiter."
            " His mythologies and powers are similar, though not identical, to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin."
        ],
        viewed_persistent=True,
    )

If your Encyclopaedia is global, you must use viewed_persistent to be able to save the viewed status of an entry.
