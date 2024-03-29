Placeholders
============

Every EncEntry can be given placeholders for the name, text, and image.
This allows you to display a locked entry without revealing what the content of the entry is.

If no specific placeholders are provided, a default text placeholder is used for the name and text.

.. code-block:: python

    about_area_51 = EncEntry(
        parent=your_new_encyclopaedia,
        name="Area 51",
        locked_name="Unknown"
        text=[
            "The base's current primary purpose is publicly unknown; however, based on historical evidence, "
            "it most likely supports the development and testing of experimental aircraft and weapons systems (black projects). "
            "The intense secrecy surrounding the base has made it the frequent subject of conspiracy theories and a central component to unidentified flying object (UFO) folklore. "
            "Although the base has never been declared a secret base, all research and occurrences in Area 51 are Top Secret/Sensitive Compartmented Information (TS/SCI). "
            "On 25 June 2013, following a Freedom of Information Act (FOIA) request filed in 2005, "
            "the CIA publicly acknowledged the existence of the base for the first time, declassifying documents detailing the history and purpose of Area 51."
        ],
        locked_text=["Classified"],
        image="area_51.png",
        locked_image="area_51_placeholder.png",
    )


Locked Image
------------

If nothing is provided for the locked_image argument, the placeholder image
will be a tinted version of the normal image. The default tint can be changed
via the `locked_image_tint` argument.

.. code-block:: python

    about_area_51 = EncEntry(
        parent=your_new_encyclopaedia,
        name="Area 51",
        locked_name="Unknown"
        text=[
            "The base's current primary purpose is publicly unknown; however, based on historical evidence, "
            "it most likely supports the development and testing of experimental aircraft and weapons systems (black projects). "
            "The intense secrecy surrounding the base has made it the frequent subject of conspiracy theories and a central component to unidentified flying object (UFO) folklore. "
            "Although the base has never been declared a secret base, all research and occurrences in Area 51 are Top Secret/Sensitive Compartmented Information (TS/SCI). "
            "On 25 June 2013, following a Freedom of Information Act (FOIA) request filed in 2005, "
            "the CIA publicly acknowledged the existence of the base for the first time, declassifying documents detailing the history and purpose of Area 51."
        ],
        locked_text=["Classified"],
        image="area_51.png",
        locked_image="area_51_placeholder.png",
        locked_image_tint=(0.2, 0.5, 0.1),
    )
