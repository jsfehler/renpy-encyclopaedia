.. _migration_to_book:

Migrating Sub-Pages to Book
===========================

Book and `Sub-Pages` have similar functionality.
Both are grouping mechanisms.

A Book is a flatter, more structured approach to grouping.
It has stricter requirements for adding pages than Sub-Pages but have
more options for managing pages as a group.

Key Differences
---------------

Display Name
~~~~~~~~~~~~

A Book has a title attribute. It's what is displayed in the list of entries.
Each page in a Book can have its own name and this can be displayed elsewhere.
On the framework's default screens it's shown on the entry screen.

Sub-Pages will display the name of the first entry in an Encyclopaedia's
list of entries. That name will also be shown on the entry screen. There
is no mechanism to have a name for the collection and a different name
for the first page.

Nesting
~~~~~~~

An EncEntry that is a sub-page of another EncEntry can have its own sub-pages.
(However, the framework's default screens have no support for this.)

A Book, on the other hand, cannot have another Book inside it.

Viewed Status
~~~~~~~~~~~~~

A Book is only considered viewed when every page in the Book has been viewed.

An EncEntry with Sub-Pages will be considered viewed once the parent EncEntry has been viewed.


Migration Example
-----------------

Before:

.. code-block:: python

    food_encyclopaedia = Encyclopaedia(name="Food")

    apples = EncEntry(
        parent=food_encyclopaedia,
        name="Apples",
        subject="Fruit",
        text="All About Apples."
    )

    EncEntry(parent=apples, name="Red Apples", text="...")
    EncEntry(parent=apples, name="Green Apples", text="...")


After:

.. code-block:: python

    food_encyclopaedia = Encyclopaedia(name="Food")

    apples_book = Book(parent=food_encyclopaedia, title="Apples", subject="Fruit")

    EncEntry(parent=apples_book, number=0, name="Apples", text="All About Apples")
    EncEntry(parent=apples_book, number=1, name="Red Apples", text="...")
    EncEntry(parent=apples_book, number=2, name="Green Apples", text="...")
