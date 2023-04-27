Manual Numbering
================

By default, entries are numbered in the order they are added to the Encyclopaedia.

However, if you need an entry to have a specific number, you can specify this when creating the entry.

WARNING: This will only work if the number you want to use has not already been automatically assigned.
(ie: If you have six entries, then for the seventh try to assign it to 4, it will fail.)

.. code-block:: python

    number_of_the_beast = EncEntry(
        parent=your_new_encyclopaedia,
        number=666,
        name="The Number of the Beast",
        text=[
            "Six hundred and sixty-six is called the 'number of the Beast' in (most manuscripts of) chapter 13 of the Book of Revelation,"
            "of the New Testament, and also in popular culture."
        ]
    )
