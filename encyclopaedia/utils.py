from renpy.display import im


def tint(image, tint_amount):
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
        tint_amount[2]
    )
    tinted_image = im.MatrixColor(
        image,
        matrix
    )

    return tinted_image
