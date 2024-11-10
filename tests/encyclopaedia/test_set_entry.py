import pytest

from encyclopaedia import EncEntry, Encyclopaedia
from encyclopaedia.exceptions_ren import UnknownEntryError


def test__change_active_entry_viewed_status_no_active():
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    with pytest.raises(ValueError):
        enc._change_active_entry_viewed_status()


def test__change_active_entry_viewed_status_locked_entry():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=True,
    )

    enc.active = e

    result = enc._change_active_entry_viewed_status()
    assert result is False


def test_set_entry_unknown_entry():
    enc = Encyclopaedia()
    another_enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    with pytest.raises(UnknownEntryError):
        another_enc.set_entry(e)
