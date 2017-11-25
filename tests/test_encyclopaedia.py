import pytest

from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry


def test_percentage_unlocked():
    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=True
        )

    assert 50.00 == enc.percentage_unlocked


def test_percentage_unlocked_empty():
    """When an encyclopaedia is empty,
    Then accessing percentage_unlocked raises an Exception.
    And provide a readable error message.
    """
    enc = Encyclopaedia()

    with pytest.raises(ZeroDivisionError) as e:
        enc.percentage_unlocked

    message = 'Cannot calculate percentage unlocked of empty Encyclopaedia'
    assert message == str(e.value)
