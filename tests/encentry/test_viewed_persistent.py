from encyclopaedia import Encyclopaedia

from renpy.game import persistent


def test_viewed_persistent_first_get(add_dummy_entries):
    """
    When viewed status is controlled by a persistent variable
    And viewed attribute has not been changed
    Then the EncEntry's viewed attribute is False
    And the persistent variable is False
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        viewed_persistent=True,
    )

    assert result[0].viewed is False
    assert persistent.Zeus_0_viewed is False


def test_viewed_persistent_get(add_dummy_entries):
    """
    When viewed status is controlled by a persistent variable
    Then the EncEntry's viewed attribute is linked to a persistent variable
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        viewed_persistent=True,
    )

    assert result[0].viewed == persistent.Zeus_0_viewed


def test_viewed_persistent_set(add_dummy_entries):
    """
    When locked status is controlled by a persistent variable
    Then the EncEntry's viewed attribute is linked to a persistent variable
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        viewed_persistent=True,
    )

    result[0].viewed = True

    assert persistent.Zeus_0_viewed is True
    assert result[0].viewed == persistent.Zeus_0_viewed
