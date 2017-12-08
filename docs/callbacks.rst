Callbacks
=========

Encyclopaedia and EncEntry have callbacks which can be used to connect events occurring in an encyclopaedia to the rest of the game.

unlock_callback
---------------

Both Encyclopadedia and EncEntry have a parameter called `unlock_callback`.

When a function is assigned to unlock_callback, that function will be called whenever a child entry is unlocked.

.. code-block:: python

    def increase_intelligence():
        nerd_points += 1

    my_encyclopaedia.unlock_callback = increase_intelligence


viewed_callback
---------------

EncEntry has a parameter called `viewed_callback`.

When a function is passed to viewed_callback, that function will be called when the entry is first viewed.

.. code-block:: python

    def kung_fu_callback(*args):
        global knows_kung_fu
        knows_kung_fu = True

    my_entry.viewed_callback = (kung_fu_callback,)

viewed_callback takes a tuple with the first item being the function and subsequent items being arguments for that function.
