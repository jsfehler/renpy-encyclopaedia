Accessing the Encyclopaedia
===========================

Screens
-------
Just creating an Encyclopaedia isn't enough. You must give players a way to view it.

The framework includes default `screens` you can use to display the Encyclopaedia's data.

The screens don't contain any of data or state control.
They can be skinned, customized, or only used as a reference. It all depends on the needs of your game.

Opening the Encyclopaedia
-------------------------

While the specifics of opening the Encyclopaedia will depend on your game, most likely you'll need to add a button somewhere.
This can be on the main menu, in-game, or wherever is appropriate for your game.

If you use the default screens, the `Action` you want to use for the button is `ShowMenu()` with 2 arguments.
The first must be the name of the screen, and the second an `Encyclopaedia` object.

The default screen's name is "encyclopaedia_list".
