Events & Callbacks
==================

Encyclopaedia and EncEntry emit events which can be subscribed to by your own callback functions.
This can be used to connect events occurring in an Encyclopaedia to the rest of the game.

Events send the source of the event to the callback function.

Encyclopaedia and EncEntry emit the "entry_unlocked" event. Occurs when any entry (or sub-entry) is unlocked.

.. code-block:: python

    greek_gods = Encyclopaedia()

    @greek_gods.on("entry_unlocked")
    def increase_intelligence(source):
        global nerd_points
        nerd_points += 1


EncEntry emits the following events:

- "unlocked". Triggered when the entry is unlocked
- "viewed". Triggered when the entry is viewed for the first time.

.. code-block:: python

    greek_gods = Encyclopaedia()

    about_zeus = EncEntry(
        parent=greek_gods,
        name="Zeus",
        text=[""]
    )

    @about_zeus.on("viewed")
    def cb(source):
        global knows_kung_fu
        knows_kung_fu = True
