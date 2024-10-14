Subject Attribute Inheritance
=============================

When an EncEntry is added to a Book its `subject` attribute is set to the
same as the Book's.

If an EncEntry already has a subject an error is raised.

.. code-block:: python

    apples_book = Book(title="Apples", subject="Fruit")

    red_apples = EncEntry(
        parent=apples_book,
        number=0,
        name="Red Apples",
        text="You can eat red apples.",
    )

    red_apples.subject == "Fruit"
