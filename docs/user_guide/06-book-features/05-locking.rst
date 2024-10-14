Locking & Unlocking
===================

Book has a separate locked status from its pages.
This can result in unexpected side-effects with an Encyclopaedia's
`show_locked_entry` parameter.

In the following example:

- The Book is locked but its page is not.
- The Encyclopaedia has the `show_locked_buttons` parameter set to True.

.. code-block:: python

    fruit_encyclopaedia = Encyclopaedia(show_locked_buttons=True)

    apples_book = Book(parent=fruit_encyclopaedia, title="Apples", locked=True)

    EncEntry(
        parent=apples_book,
        number=0,
        name="Red Apples",
        text="You can eat red apples.",
        locked=False,
    )

Result:

- The Book will be present in the list of entries.
- The page will not be accessible, even though the page is not locked.

In this next example:

- The Book is locked but its page is not.
- The Encyclopaedia has the `show_locked_buttons` and `show_locked_entry` parameters set to True.

.. code-block:: python

    fruit_encyclopaedia = Encyclopaedia(show_locked_buttons=True, show_locked_entry=True)

    apples_book = Book(parent=fruit_encyclopaedia, title="Apples", locked=True)

    EncEntry(
        parent=apples_book,
        number=0,
        name="Red Apples",
        text="You can eat red apples.",
        locked=False,
    )

Result:

- The Book will be present in the list of entries.
- The page will be accessible because it is not locked, even though the Book is locked.

If the page was locked, its placeholders would be displayed instead.
