Translations
============

The easiest way to support Translations is to create multiple Encyclopaedias for each language in your game.

However, this alone won't change the labels used on the screens. By default these are all in English.

Modifying an Encyclopaedia's labels can be done using the Labels object.
Every Encyclopaedia is created with a default one that can be replaced.

To customize the labels, create a new Labels object, rewrite the labels inside it, and assign the object to your Encyclopaedia.

The following attributes are available:

- percentage_label (str): Placed next to the percentage unlocked number

- page_label (str): Placed before the entry page displayed

- page_separator_label (str): Placed in-between the current page number and the total page number

- sort_number_label (str): Label for Number Sorting

- sort_alphabetical_label (str): Label for Alphabetical sorting

- sort_reverse_alphabetical_label (str): Label for Reverse Alphabetical sorting

- sort_subject_label (str): Label for Subject sorting

- sort_unread_label (str): Label for Unread sorting

- unread_entry_label (str): Default for the tag next to unread entries

- locked_entry_label (str): Default for a "Locked Entry" button

.. code-block:: python

    # English
    en_encyclopaedia = Encyclopaedia()

    # French
    fr_encyclopaedia = Encyclopaedia()

    fr_labels = Labels(fr_encyclopaedia)
    fr_labels.sort_alphabetical_label = "De A à Z"

    fr_encyclopaedia.labels = fr_labels
