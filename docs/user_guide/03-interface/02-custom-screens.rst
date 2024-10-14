.. _custom_screens:

Customizing Screens
===================

In the framework an Encyclopaedia's data and GUI are decoupled.
An Encyclopaedia does not know anything about how its data will be displayed,
except for the name of the screens used.

Skinning
--------

Inside encyclopaedia/screens.rpy, there is a section below the following text:

.. code-block:: python

    ######################
    # Encyclopaedia Styles
    ######################

This section contains the various styles used by the default screens.
Their properties can be adjusted to change the colours, fonts, and other
parameters.

Custom Screen
-------------

The default screens can also be edited directly or outright replaced.

In the following toy example, instead of textbuttons for each entry, we're going
to use an imagebutton.

.. code-block:: renpy

    screen custom_encyclopaedia_screen(enc):
        vbox:
            for entry in enc.current_entries:
                imagebutton idle "my_image.png" action enc.SetEntry(entry)

    init python:
        greek_mythology = Encyclopaedia(name="Greek Mythology", list_screen="custom_encyclopaedia_screen")

    screen open_encyclopaedia():
        textbutton "Open Encyclopaedia" action ShowMenu(greek_mythology.list_screen, greek_mythology)

    label start:
        show screen open_encyclopaedia

        "I sure love having a game with an encyclopaedia."

        return
