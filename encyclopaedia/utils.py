from typing import cast, Union

from renpy.python import RevertableList


def string_to_list(given_text: Union[str, list[str]]) -> list[str]:
    """Turn a string into a list containing that string.

    Each list item represents a paragraph.
    If a string is given, convert it to a list,
    assuming a string with no list = one paragraph.

    Args:
        given_text

    Returns:
        list[str]
    """
    # If the text is already in a list, just return it.
    if type(given_text) in (RevertableList, list):
        return cast(list[str], given_text)

    return [cast(str, given_text)]
