Screen Actions
==============

In order to work with `Screens and Screen Language <https://www.renpy.org/doc/html/screens.html>`_,
an Encyclopaedia has a collection of custom `Screen Actions <https://www.renpy.org/doc/html/screen_actions.html>`_
available.


PreviousEntry
-------------

Changes the currently active EncEntry to the previous one.
If the currently active EncEntry is the first one, this action will do nothing.

.. code-block:: python

        textbutton "Previous Entry" action my_encyclopaedia.PreviousEntry()

NextEntry
---------

Changes the currently active EncEntry to the next one.
If the currently active EncEntry is the last one, this action will do nothing.

.. code-block:: python

    textbutton "Next Entry" action my_encyclopaedia.NextEntry()


PreviousPage
------------

Changes the currently active EncEntry's Sub-Page to the previous one.
If the currently active Sub-Page is the first one, this action will do nothing.

.. code-block:: python

    textbutton "Previous Page" action my_encyclopaedia.PreviousPage()


NextPage
--------

Changes the currently active EncEntry's Sub-Page to the next one.
If the currently active Sub-Page is the last one, this action will do nothing.

.. code-block:: python

    textbutton "Next Page" action my_encyclopaedia.NextPage()


Sort
----

Sorts the encyclopaedia by the sorting mode provided.

Takes a valid sorting mode as an argument.

.. code-block:: python

    textbutton "Sort By Unread" action my_encyclopaedia.Sort(Encyclopaedia.SORT_UNREAD)

SetEntry
--------

Set an EncEntry as the active entry, then opens the Encyclopaedia's Entry Screen.

.. code-block:: python

    textbutton "Open an Entry" action my_encyclopaedia.SetEntry(my_enc_entry)

ResetSubPage
------------

Sets the currently active EncEntry's Sub-Page to the first page.

.. code-block:: python

    textbutton "Return to First Page" action my_encyclopaedia.ResetSubPage()


ToggleShowLockedButtons
-----------------------

Toggles if locked Entries will be visible in the list of Entries.

.. code-block:: python

    textbutton "Show Locked Buttons" action my_encyclopaedia.ToggleShowLockedButtons()

ToggleShowLockedEntry
---------------------

Toggles if locked Entries can be viewed.

.. code-block:: python

    textbutton "Show Locked Entries" action my_encyclopaedia.ToggleShowLockedEntry()

FilterBySubject
---------------

Create a filter for EncEntry in an Encyclopaedia, based on the "subject" attribute.

.. code-block:: python

    textbutton "Only Show Blue Things" action my_encyclopaedia.FilterBySubject("Blue")

ClearFilter
-----------

If a filter is active, this will clear it.

.. code-block:: python

    textbutton "Clear Filter" action my_encyclopaedia.ClearFilter()
