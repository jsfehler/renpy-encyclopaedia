Locking and Unlocking Entries
=============================

By default, all EncEntry objects are unlocked and can be viewed by players at any time.
However, when creating an EncEntry the `locked` argument can be used, effectively hiding the entry.",

.. code-block:: python

    about_zeus = EncEntry(
        parent=your_new_encyclopaedia,
        name="Zeus",
        text=[
            "Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus."
            " His name is cognate with the first element of his Roman equivalent Jupiter."
            " His mythologies and powers are similar, though not identical, to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin."
        ],
        locked=True
    )

The entry will be locked until its locked attribute is set to False.

.. code-block:: python

    about_zeus.locked = False


Unlocking is a one-way street. Once en entry has been unlocked, it cannot be relocked.
Setting an unlocked entry's locked attribute back to True will not hide it.

In order to tie an EncEntry's locked state to a persistent variable, add the "locked_persistent" argument

.. code-block:: python

    about_zeus = EncEntry(
        parent=your_new_encyclopaedia,
        name="Zeus",
        text=[
            "Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus."
            " His name is cognate with the first element of his Roman equivalent Jupiter."
            " His mythologies and powers are similar, though not identical, to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin."
        ],
        locked=True,
        locked_persistent=True
    )

If you Encyclopaedia is global, you must use the locked_persistent argument.
