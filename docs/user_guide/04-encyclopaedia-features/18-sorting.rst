Sorting
=======

The entries in an Encyclopaedia can be sorted in the following ways:

- By Number

- Alphabetically

- Reverse Alphabetically

- By Subject

- By Viewed status

When setting the sorting mode, the `SortMode` Enum must be used.
The following names are valid:

  - SortMode.NUMBER

  - SortMode.ALPHABETICAL

  - SortMode.REVERSE_ALPHABETICAL

  - SortMode.SUBJECT

  - SortMode.UNREAD

Change Sorting Mode
-------------------

An Encyclopaedia has the `sort()` method and `Sort()` Action available.
Changing the value of the `sorting_mode` attribute also changes the sorting mode.

.. code-block:: python

    my_encyclopaedia.sorting_mode = SortMode.SUBJECT
    my_encyclopaedia.sort(SortMode.SUBJECT)


.. code-block:: python

    screen foo():
        textbutton "Sort by Subject" my_encyclopaedia.Sort(SortMode.SUBJECT)

Changing the default sorting mode
---------------------------------

By default, when an Encyclopaedia is opened the sorting mode is by Number.

This can be changed when creating a new Encyclopaedia with the `sorting_mode` argument.

.. code-block:: python

    your_new_encyclopaedia = Encyclopaedia(
        sorting_mode=SortMode.ALPHABETICAL,
    )
