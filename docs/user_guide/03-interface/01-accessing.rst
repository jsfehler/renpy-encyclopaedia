Accessing the Encyclopaedia
===========================

By default, an Encyclopaedia uses a screen called `encyclopaedia_list` to
display its contents.

Anything in Ren'Py that is used to open screens can be used to open this screen.

Generally, the `Action <https://www.renpy.org/doc/html/screen_actions.html>`_
you want to use is
`ShowMenu() <https://www.renpy.org/doc/html/screen_actions.html#ShowMenu>`_ with 2 arguments.
The first argument must be the name of the screen and the second an `Encyclopaedia` instance.

An Encyclopaedia stores the name of the screen it uses in a variable called `list_screen`.
Using this variable is recommended to ensure you always open the correct screen.

.. code-block:: renpy

    my_encyclopaedia = Encyclopaedia()

    ShowMenu(my_encyclopaedia.list_screen, my_encyclopaedia)


See the Hyperlinks section for a way to open an Encyclopaedia directly from in-game dialogue.
See the Screens section for more information on how an Encyclopaedia displays its content.
