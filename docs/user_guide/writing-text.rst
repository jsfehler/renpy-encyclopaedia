Writing Text
============

When creating an entry, you can use either a single string or a list of strings.
If a single string is given it will simply be placed inside a list as the first and only item.

On the default entry screen, each list item is treated as a paragraph with a line break.

Remember, there's a difference between how text looks in your script file and how it looks on screen. Take the following:

.. code-block:: python

    text=[
        "X."
        "Y."
        "Z."
    ]

Although they're broken into multiple lines, there's no comma separating them. They will be one list item and displayed as one paragraph.
