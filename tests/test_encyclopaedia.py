import pytest

from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry


def test_add_subpage():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False
    )

    ee = EncEntry(
        parent=e,
        name="A Sub-Page",
        text=["Test Text"],
        locked=False
    )

    assert [[1, e], [2, ee]] == e.sub_entry_list


def test_current_entries_show_unlocked():
    """With filtering off and show_locked_buttons set to False,
    Encyclopaedia.current_entries property should return
    Encyclopaedia.unlocked_entries.
    """

    enc = Encyclopaedia()

    expected_list = []

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )
        expected_list.append(e)

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=True
        )

    assert expected_list == enc.current_entries


def test_current_entries_show_all():
    """With filtering off and show_locked_buttons set to True,
    Encyclopaedia.current_entries property should return
    Encyclopaedia.all_entries.
    """

    enc = Encyclopaedia(show_locked_buttons=True)

    expected_list = []

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )
        expected_list.append(e)

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=True
        )
        expected_list.append(e)

    assert expected_list == enc.current_entries


def test_percentage_unlocked():
    """Base unit test for the
    Encyclopaedia.percentage_unlocked property.
    """

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
