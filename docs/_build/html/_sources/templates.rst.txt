Templates
=========

When many entries have identical parameters, such as subject, EncEntryTemplate can be used
to reduce the amount of duplication necessary.


.. code-block:: python

    about_gods = Encyclopaedia()

    GreekGodsEntry = EncEntryTemplate(parent=about_gods, subject="Greek Gods")

    about_zeus = GreekGodsEntry(name="Zeus")


Any valid argument for EncEntry can be used in EncEntryTemplate.
