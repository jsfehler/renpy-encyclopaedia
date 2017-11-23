Placeholders
============

Every EncEntry can be given placeholders for the name, text, and image.
This allows you to display a locked entry without revealing what the content of the entry is.

If no specific placeholders are provided, a default text placeholder is used for the name and text.
The default placeholder image will be a dark tinted version of the normal image.

.. code-block:: python

    about_zeus = EncEntry(
        parent=your_new_encyclopaedia,
        name="Zeus",
        locked_name="Unknown"
        text=[
            "Zeus is the sky and thunder god in ancient Greek religion, who ruled as king of the gods of Mount Olympus."
            " His name is cognate with the first element of his Roman equivalent Jupiter."
            " His mythologies and powers are similar, though not identical, to those of Indo-European deities such as Indra, Jupiter, Perun, Thor, and Odin."
        ],
        locked_text=["Classified"]
    )
