Sorting
=======

The list of entries in an Encyclopaedia can be sorted by:

- Alphabetical order

- Reverse Alphabetical order

- Subject

- Number

- Unread

Changing the sorting mode is handled by the Encyclopaedia.Sort() action.

Changing the default sorting mode
---------------------------------

By default, when an Encyclopaedia is opened the sorting mode is by Number.

This can be changed when creating a new Encyclopaedia with the `sorting_mode` argument.

.. code-block:: python

    your_new_encyclopaedia = Encyclopaedia(
        sorting_mode=Encyclopaedia.SORT_ALPHABETICAL
    )

The following parameters are valid:

    - Encyclopaedia.SORT_NUMBER

    - Encyclopaedia.SORT_ALPHABETICAL

    - Encyclopaedia.SORT_REVERSE_ALPHABETICAL

    - Encyclopaedia.SORT_SUBJECT

    - Encyclopaedia.SORT_UNREAD
