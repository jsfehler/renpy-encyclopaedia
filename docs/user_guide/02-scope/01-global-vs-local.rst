Global Scope vs Local Scope
===========================

An Encyclopaedia can retain state independent of saved games, or be bound to a saved game.
State in this situation refers to the viewed and locked status of any entry in the Encyclopaedia.

A global Encyclopaedia is initialized when the application is opened and can be accessed even if the player hasn't started a new game yet.
(e.g., From the main menu). Since it runs outside of the normal game flow, a global Encyclopaedia must use `persistent data <https://www.renpy.org/doc/html/persistent.html>`_ to save their state.
As a result, a global Encyclopaedia's state will not be bound to any particular save game.

For a local Encyclopaedia, state will be different across every saved game. State is saved when the player saves their game.
A local Encyclopaedia should only be accessed from within a game, never from the main menu.

A global Encyclopaedia must be created inside an `init python <https://www.renpy.org/doc/html/python.html#init-python-statement>`_ block.
A local Encyclopaedia must be created inside a `python <https://www.renpy.org/doc/html/python.html#python-statement>`_ block, inside a label (usually the start label).


Global:

.. code-block:: python

    init python:
        your_new_encyclopaedia = Encyclopaedia()

Local:

.. code-block:: python

    label start:
        python:
            your_new_encyclopaedia = Encyclopaedia()
