Achievement Integration
=======================

Ren'Py's Achievements system can be used to control the locked state of an Entry.
The AchievementEncEntry class uses a single Achievement name to control
its locked state.

This is **not** a replacement for Ren'Py's achievement system.
It only allows you to manage the state of an EncEntry using an
Achievement's status.

.. note:: AchievementEncEntry does not emit the "unlocked" event.

.. note:: AchievementEncEntry does not cause the parent Encyclopaedia to emit the "entry_unlocked" event.


.. code-block:: python

    achievement_read_all_books = "read_all_books"

    achievement.register(achievement_read_all_books)

    reader_encyclopaedia = Encyclopaedia()

    read_all_the_books_entry = AchievementEncEntry(
        achievement=achievement_read_all_books,
        parent=reader_encyclopaedia,
        name="Looks Like We Got Ourselves A Reader",
        text="Read all the books."
    )

    >>> read_all_the_books_entry.locked == True

    achievement.grant(achievement_read_all_books)

    >>> read_all_the_books_entry.locked == False
