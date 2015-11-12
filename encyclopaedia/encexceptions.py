class MissingImageError(Exception):
    """
    Occurs if you try to tint an Entry's image when
    there is no image set.
    """
    pass