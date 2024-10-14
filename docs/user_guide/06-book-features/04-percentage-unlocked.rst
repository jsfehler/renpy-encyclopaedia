Percentage Unlocked
===================

The percentage_unlocked attribute returns a number between 0.0 and 1.0,
representing the number of unlocked pages out of the total number of pages.

.. code-block:: python

    apples_book = Book(title="Apples")

    EncEntry(
        parent=apples_book,
        number=0,
        name="Red Apples",
        text="You can eat red apples.",
    )
    EncEntry(
        parent=apples_book,
        number=1,
        name="Green Apples",
        text="You can eat green apples.",
        locked=True,
    )

    book.percentage_unlocked == 0.5
