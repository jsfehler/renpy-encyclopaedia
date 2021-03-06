from renpy.display import im
from renpy.python import RevertableList


def enc_tint(image, tint_amount):
    """Tint an image.

    If the EncEntry has an image but no locked image, tint the image
    and use it as the locked image.

    Args:
        image: The image to tint
        tint_amount: Tuple for the RGB values to tint the image

    Returns:
        tinted image
    """

    matrix = im.matrix.tint(
        tint_amount[0],
        tint_amount[1],
        tint_amount[2],
    )

    tinted_image = im.MatrixColor(
        image,
        matrix,
    )

    return tinted_image


def string_to_list(given_text):  # type: (Optional[str, List]) -> List
    """Turn a string into a list containing that string.

    Each list item represents a paragraph.
    If a string is given, convert it to a list,
    assuming a string with no list = one paragraph.

    Args:
        given_text [str|list]

    Returns:
        list
    """
    # If the text is already in a list, just return it.
    if type(given_text) in (RevertableList, list):
        return given_text
    return [given_text]
