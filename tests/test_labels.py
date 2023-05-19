import pytest

from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry
from encyclopaedia import constants_ren


def test_percentage_unlocked_label():
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

    assert "50%" == enc.labels.percentage_unlocked


def test_entry_current_page():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False
    )

    enc.SetEntry(e)()

    assert "Page 1 / 1" == enc.labels.entry_current_page


def test_entry_current_page_closed_page():
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False
    )

    with pytest.raises(AttributeError) as e:
        enc.labels.entry_current_page

    message = "Cannot display Entry's current page when no entry is open."
    assert message == str(e.value)


def test_sorting_mode_label():
    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            subject="Test Subject",
        )

    assert "Number" == enc.labels.sorting_mode

    enc.Sort(constants_ren.SortMode.ALPHABETICAL)()
    assert "A to Z" == enc.labels.sorting_mode

    enc.Sort(constants_ren.SortMode.REVERSE_ALPHABETICAL)()
    assert "Z to A" == enc.labels.sorting_mode

    enc.Sort(constants_ren.SortMode.SUBJECT)()
    assert "Subject" == enc.labels.sorting_mode

    enc.Sort(constants_ren.SortMode.UNREAD)()
    assert "Unread" == enc.labels.sorting_mode
