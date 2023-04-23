Accessing the Encyclopaedia
===========================

Just creating an Encyclopaedia isn't enough. You must give players a way to view it.

Opening the Encyclopaedia
-------------------------

While the specifics of opening the Encyclopaedia will depend on your game, most likely you'll need to add a button somewhere.
This can be on the main menu, in-game, or wherever is appropriate for your game.

If you use the default screens, the `Action <https://www.renpy.org/doc/html/screen_actions.html>`_
you want to use for the button is `ShowMenu() <https://www.renpy.org/doc/html/screen_actions.html#ShowMenu>`_ with 2 arguments.
The first must be the name of the screen, and the second an `Encyclopaedia` object.

The default screen used is called "encyclopaedia_list".

Screens
-------
The framework includes default `screens <https://www.renpy.org/doc/html/screens.html>`_ you can use to display the Encyclopaedia's data.

They can be skinned, customized, or only used as a reference. It all depends on the needs of your game.

The screens are located in encyclopaedia_screens.rpy.