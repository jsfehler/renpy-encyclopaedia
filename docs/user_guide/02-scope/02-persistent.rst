Persistent Data
===============

If your Encyclopaedia is global, you must set the `viewed_persistent` and `locked_persistent`
arguments to True to be able to save the entry's status.

.. code-block:: python

    your_new_encyclopaedia = Encyclopaedia()

    about_zeus = EncEntry(
        parent=your_new_encyclopaedia,
        name="Zeus",
        text=[
            "Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus."
            " His name is cognate with the first element of his Roman equivalent Jupiter."
            " His mythologies and powers are similar, though not identical, to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin."
        ],
        viewed_persistent=True,
        locked_persistent=True,
    )
