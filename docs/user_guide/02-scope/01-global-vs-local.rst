Global Scope vs Local Scope
===========================

Generally, you'll want your Encyclopaedia to retain state.
State in this context refers to the viewed and locked status of an EncEntry
in an Encyclopaedia. Your Encyclopaedia can be configured to retain state
independent of saved games (globally) or retain state inside a saved game (locally).

Global Encyclopaedia
--------------------

A global Encyclopaedia is initialized when the application is opened and can be
accessed from menus outside the normal game flow. (e.g., From the main menu).
They use `persistent data <https://www.renpy.org/doc/html/persistent.html>`_ to save their state.
As a result, a global Encyclopaedia's state can never be bound to any particular save game.

A global Encyclopaedia must be created inside an `init python <https://www.renpy.org/doc/html/python.html#init-python-statement>`_ block.

Example:

.. code-block:: python

    init python:
        your_new_encyclopaedia = Encyclopaedia()

Local Encyclopaedia
-------------------

For a local Encyclopaedia, state will be different across every saved game.
State is only saved when the player saves their game.
A local Encyclopaedia should only be accessed from within a game, never from outside the normal game flow.

A local Encyclopaedia must be created inside a `python <https://www.renpy.org/doc/html/python.html#python-statement>`_ block, inside a label (usually the start label).

Example:

.. code-block:: python

    label start:
        python:
            your_new_encyclopaedia = Encyclopaedia()
