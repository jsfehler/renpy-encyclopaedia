Screen Actions
==============

In order to work with `Screens and Screen Language <https://www.renpy.org/doc/html/screens.html>`_,
an Encyclopaedia has a collection of custom `Screen Actions <https://www.renpy.org/doc/html/screen_actions.html>`_
available.

Changing Entries
----------------

SetEntry
~~~~~~~~

Set an EncEntry as the active entry, then opens the Encyclopaedia's Entry Screen.

.. code-block:: renpy

        init python:
            about_gods = Encyclopaedia()
            about_zeus = EncEntry()

        screen my_screen():
            textbutton "Open an Entry" action about_gods.SetEntry(about_zeus)

PreviousEntry
~~~~~~~~~~~~~

Changes the currently active EncEntry to the previous one.
If the currently active EncEntry is the first one, this action will do nothing.

.. code-block:: renpy

        init python:
            about_gods = Encyclopaedia()

        screen my_screen():
            textbutton "Previous Entry" action about_gods.PreviousEntry()

NextEntry
~~~~~~~~~

Changes the currently active EncEntry to the next one.
If the currently active EncEntry is the last one, this action will do nothing.

.. code-block:: renpy

      init python:
          about_gods = Encyclopaedia()

      screen my_screen():
          textbutton "Next Entry" action about_gods.NextEntry()


Changing Pages
--------------

PreviousPage
~~~~~~~~~~~~

Changes the currently active EncEntry's Sub-Page to the previous one.
If the currently active Sub-Page is the first one, this action will do nothing.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Previous Page" action about_gods.PreviousPage()

NextPage
~~~~~~~~

Changes the currently active EncEntry's Sub-Page to the next one.
If the currently active Sub-Page is the last one, this action will do nothing.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Next Page" action about_gods.NextPage()


Changing State
--------------

CloseActiveEntry
~~~~~~~~~~~~~~~~

Safely close the active EncEntry. This Action ensures all steps are taken to
close the entry.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Close Entry" action about_gods.CloseActiveEntry()

ResetSubPage
~~~~~~~~~~~~

Set the currently active EncEntry's Sub-Page to the first page.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Return to First Page" action about_gods.ResetSubPage()


Sorting & Filtering
-------------------

Sort
~~~~

Sorts the encyclopaedia by the sorting mode provided.

Takes a SortMode attribute as an argument.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Sort By Unread" action about_gods.Sort(SortMode.UNREAD)

FilterBySubject
~~~~~~~~~~~~~~~

Create a filter for EncEntry in an Encyclopaedia, based on the "subject" attribute.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Only Show Blue Things" action about_gods.FilterBySubject("Blue")

ClearFilter
~~~~~~~~~~~

If a filter is active, this will clear it.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Clear Filter" action about_gods.ClearFilter()

ToggleShowLockedButtons
~~~~~~~~~~~~~~~~~~~~~~~

Toggle if locked Entries will be visible in the list of Entries.

This action is generally used for testing and debugging.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Show Locked Buttons" action about_gods.ToggleShowLockedButtons()

ToggleShowLockedEntry
~~~~~~~~~~~~~~~~~~~~~

Toggle if locked Entries can be viewed on the Entry screen.

This action is generally used for testing and debugging.

.. code-block:: renpy

    init python:
        about_gods = Encyclopaedia()

    screen my_screen():
        textbutton "Show Locked Entries" action about_gods.ToggleShowLockedEntry()
