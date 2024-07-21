Achievement Integration
=======================

Ren'Py's Achievements system can be used to control the locked state of an Entry.
The AchievementEncEntry class uses a single Achievement name to control
its locked state.

This is **not** a replacement for Ren'Py's achievement system.
It only allows you to manage the state of an EncEntry using an
Achievement's status.

.. code-block:: python

    achievement.register("read_all_the_books")

    read_all_the_books_entry = AchievementEncEntry(
        achievement="read_all_the_books",
        parent=your_new_encyclopaedia,
        name="Looks Like We Got Ourselves A Reader",
        text="Read all the books."
    )

    >>> read_all_the_books_entry.locked == True

    achievement.grant("read_all_the_books")

    >>> read_all_the_books_entry.locked == False
