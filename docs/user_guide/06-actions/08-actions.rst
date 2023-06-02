Screen Actions
==============

In order to work with `Screens and Screen Language <https://www.renpy.org/doc/html/screens.html>`_,
an Encyclopaedia has a collection of custom `Screen Actions <https://www.renpy.org/doc/html/screen_actions.html>`_
available.

PreviousEntry
-------------

Changes the currently active EncEntry to the previous one.
If the currently active EncEntry is the first one, this action will do nothing.

.. code-block:: renpy

        textbutton "Previous Entry" action my_encyclopaedia.PreviousEntry()

NextEntry
---------

Changes the currently active EncEntry to the next one.
If the currently active EncEntry is the last one, this action will do nothing.

.. code-block:: renpy

    textbutton "Next Entry" action my_encyclopaedia.NextEntry()

PreviousPage
------------

Changes the currently active EncEntry's Sub-Page to the previous one.
If the currently active Sub-Page is the first one, this action will do nothing.

.. code-block:: renpy

    textbutton "Previous Page" action my_encyclopaedia.PreviousPage()

NextPage
--------

Changes the currently active EncEntry's Sub-Page to the next one.
If the currently active Sub-Page is the last one, this action will do nothing.

.. code-block:: renpy

    textbutton "Next Page" action my_encyclopaedia.NextPage()

Sort
----

Sorts the encyclopaedia by the sorting mode provided.

Takes a valid sorting mode as an argument.

.. code-block:: renpy

    textbutton "Sort By Unread" action my_encyclopaedia.Sort(SortMode.UNREAD)

SetEntry
--------

Set an EncEntry as the active entry, then opens the Encyclopaedia's Entry Screen.

.. code-block:: renpy

    textbutton "Open an Entry" action my_encyclopaedia.SetEntry(my_enc_entry)

CloseActiveEntry
----------------

Safely close the active EncEntry. This Action ensures all steps are taken to
close the entry.

.. code-block:: renpy

    textbutton "Close Entry" action my_encyclopaedia.CloseActiveEntry()

ResetSubPage
------------

Set the currently active EncEntry's Sub-Page to the first page.

.. code-block:: renpy

    textbutton "Return to First Page" action my_encyclopaedia.ResetSubPage()

FilterBySubject
---------------

Create a filter for EncEntry in an Encyclopaedia, based on the "subject" attribute.

.. code-block:: renpy

    textbutton "Only Show Blue Things" action my_encyclopaedia.FilterBySubject("Blue")

ClearFilter
-----------

If a filter is active, this will clear it.

.. code-block:: renpy

    textbutton "Clear Filter" action my_encyclopaedia.ClearFilter()

ToggleShowLockedButtons
-----------------------

Toggle if locked Entries will be visible in the list of Entries.

This action is generally used for testing and debugging.

.. code-block:: renpy

    textbutton "Show Locked Buttons" action my_encyclopaedia.ToggleShowLockedButtons()

ToggleShowLockedEntry
---------------------

Toggle if locked Entries can be viewed on the Entry screen.

This action is generally used for testing and debugging.

.. code-block:: renpy

    textbutton "Show Locked Entries" action my_encyclopaedia.ToggleShowLockedEntry()
