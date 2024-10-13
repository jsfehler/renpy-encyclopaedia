Access an Encyclopaedia
=======================

The framework includes a default `screen <https://www.renpy.org/doc/html/screens.html>`_
to display and interact with an Encyclopaedia.
Anything in Ren'Py that is used to open screens can be used to open this screen.

Generally, the `Action <https://www.renpy.org/doc/html/screen_actions.html>`_
you want to use is
`ShowMenu() <https://www.renpy.org/doc/html/screen_actions.html#ShowMenu>`_ with 2 arguments.
The first argument must be the name of the screen and the second an `Encyclopaedia` instance.

An Encyclopaedia stores the name of the screen it uses in a variable called `list_screen`.
Using this variable is recommended to ensure you always open the correct screen.

In the following example, a screen is created with a button to call ShowMenu.
The screen is then shown to the player. This allows the player to open
the encyclopaedia.

.. code-block:: renpy
    init python:
        greek_mythology = Encyclopaedia(name="Greek Mythology")

    screen open_encyclopaedia():
        textbutton "Open Encyclopaedia" action ShowMenu(greek_mythology.list_screen, greek_mythology)

    label start:
        show screen open_encyclopaedia

        "I sure love having a game with an encyclopaedia."

        return

Further Reading
---------------

See the :ref:`Default Screens <default_screens>` section for more information
on how an Encyclopaedia displays its content.

See the :ref:`Customizing Screens <custom_screens>` section for more information on creating custom screens.

See the :ref:`Hyperlinks <hyperlinks>` section for a way to open an
Encyclopaedia directly from in-game dialogue.
