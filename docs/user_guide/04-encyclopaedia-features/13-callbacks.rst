Events & Callbacks
==================

The Encyclopaedia and EncEntry classes emit events which can be subscribed to
by your own callback functions. This allows you to directly connect things
happening in an Encyclopaedia to things happening in your game.

In the following example, a screen is shown whenever an entry is unlocked:

.. code-block:: renpy

    # Shown as part of a callback when an entry is unlocked.
    screen notify_entry_unlocked():
        text _("New Entry Unlocked") xalign 0.98 yalign 0.02

        timer 2.0 action Hide('notify_entry_unlocked')

    init python:
        greek_gods = Encyclopaedia()

        @greek_gods.on("entry_unlocked")
        def notify_entry_unlocked(source):
            """This function is called when an entry is unlocked."""
            renpy.show_screen('notify_entry_unlocked')

Encyclopaedia emits the following event:

- `entry_unlocked`: Triggered when any Entry inside the Encyclopaedia is unlocked.

EncEntry emits the following events:

- `unlocked`: Triggered when the entry is unlocked
- `viewed`: Triggered when the entry is viewed for the first time.
- `entry_unlocked`: Triggered when any page inside the Entry is unlocked.

Writing Callback Functions
--------------------------

Events send the source of the event (i.e.: The Encyclopaedia or EncEntry instance)
to the callback function. Consequently, your callback function must take one
positional argument:

.. code-block:: python

    def my_callback(source):
        pass

Callback functions must be registered. In a global Encyclopaedia, you can use
the `on` decorator function.

Example:

.. code-block:: renpy

    init python:
        greek_gods = Encyclopaedia()

        about_zeus = EncEntry(
            parent=greek_gods,
            name="Zeus",
            text=[""],
        )

        @about_zeus.on("viewed")
        def lightning_strike(source):
            """Called when the about_zeus entry is viewed for the first time."""
            pass

However, a local Encyclopaedia is a bit different. You don't want the callback
function to be saved since it can interfere with Ren'Py's save/load system.
Instead, it must be placed in an init python block.

Example:

.. code-block:: renpy

    init python:
        def lightning_strike(source):
            """Called when the about_zeus entry is viewed for the first time."""
            pass

    label start:
      python:
          greek_gods = Encyclopaedia()

          about_zeus = EncEntry(
              parent=greek_gods,
              name="Zeus",
              text=[""],
          )

          about_zeus.on("viewed")(lightning_strike)
