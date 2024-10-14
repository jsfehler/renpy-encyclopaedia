Word Count
==========

The word_count attribute returns the total word count of every page in the
Book. It is only recalculated when pages are added, thus safe to call
whenever necessary, even for pages with large amounts of text.

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
    )

    book.word_count == 10
