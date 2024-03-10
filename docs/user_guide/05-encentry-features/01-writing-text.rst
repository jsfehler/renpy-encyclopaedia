Writing Text
============

When writing the text for an entry, you can use either:
  - A single string
  - A list of strings

If a single string is used it will be placed inside a list as the first and only item.

On the default entry screen, each list item is treated as a paragraph and given a line break.

Remember, there's a difference between how text looks in your script file and how it looks on screen. Take the following:

.. code-block:: python

    some_text = [
        "This is the first paragraph's text."
        "This is the second paragraph's text."
        "This is the third paragraph's text."
    ]

Although they're broken into multiple lines, there's no comma separating them. They're one list item and will be displayed as one paragraph.

Using Triple Quoted Strings Effectively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Triple quoted strings allow you to write large blocks of text with paragraphs, but have several limitations.

In the following example, when the text block is displayed in-game there will be whitespace
on the left and line breaks after each line, even though the intention is for them to be one paragraph.

.. code-block:: renpy

    init python:
        about_maccabees = """
        The Maccabees were a group of Jewish rebel warriors who took control of Judea,
        which at the time was part of the Seleucid Empire.
        They founded the Hasmonean dynasty, which ruled from 167 to 37 BCE, being a
        fully independent kingdom from 104 to 63 BCE.

        They reasserted the Jewish religion, expanded the boundaries of Judea by conquest,
        and reduced the influence of Hellenism and Hellenistic Judaism.
        """

     some_entry = EncEntry(name="Maccabees", text=some_text)

Removing the whitespace and only breaking on paragraphs will result in the text
being displayed correctly in-game, but can make for difficult to maintain code:

.. code-block:: renpy

    init python:
        about_maccabees = """
    The Maccabees were a group of Jewish rebel warriors who took control of Judea, which at the time was part of the Seleucid Empire. They founded the Hasmonean dynasty, which ruled from 167 to 37 BCE, being a fully independent kingdom from 104 to 63 BCE.

    They reasserted the Jewish religion, expanded the boundaries of Judea by conquest, and reduced the influence of Hellenism and Hellenistic Judaism.
        """

        some_entry = EncEntry(name="Maccabees", text=some_text)


To solve this, the Encyclopaedia framework has a function called ``enc_utils.text_block``.
When used, extra whitespace and non-paragraph linebreaks are removed. Text will be
displayed correctly while allowing for better management of the blocks of text.

.. code-block:: renpy

     init python:
         about_maccabees = enc_utils.text_block("""\
         The Maccabees were a group of Jewish rebel warriors who took control of Judea,
         which at the time was part of the Seleucid Empire.
         They founded the Hasmonean dynasty, which ruled from 167 to 37 BCE, being a
         fully independent kingdom from 104 to 63 BCE.

         They reasserted the Jewish religion, expanded the boundaries of Judea by conquest,
         and reduced the influence of Hellenism and Hellenistic Judaism.
         """)

         some_entry = EncEntry(name="Maccabees", text=some_text)
