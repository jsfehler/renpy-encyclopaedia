import pytest

from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry

from renpy.game import persistent


def test_locked_persistent_first_get(add_dummy_entries):
    """
    When locked status is controlled by a persistent variable
    And locked attribute has not been changed
    Then the persistent variable is set to the value of the locked attribute
    And the EncEntry's locked variable is set to the value of the locked attribute
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        locked=False,
        locked_persistent=True,
    )

    assert result[0].locked is False
    assert persistent.Zeus_0_locked is False


def test_locked_persistent_get(add_dummy_entries):
    """
    When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute is linked to a persistent variable
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        locked=True,
        locked_persistent=True,
    )

    assert result[0].locked == persistent.Zeus_0_locked


def test_locked_persistent_set(add_dummy_entries):
    """
    When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute is linked to a persistent variable
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        locked=True,
        locked_persistent=True,
    )

    result[0].locked = False

    assert persistent.Zeus_0_locked is False
    assert result[0].locked == persistent.Zeus_0_locked
