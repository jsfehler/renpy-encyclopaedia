import pytest

from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry


def test_next_page():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    ee = EncEntry(
        parent=e,
        name="Sub1",
        text=["Test Text"],
    )

    EncEntry(
        parent=e,
        name="Sub2",
        text=["Test Text"],
    )

    enc.SetEntry(e)()

    assert e == enc.active
    assert enc.active._unlocked_page_index == 0

    enc.NextPage()()

    assert enc.active._unlocked_page_index == 1
    assert ee == e.current_page


def test_next_page_no_active():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    EncEntry(
        parent=e,
        name="Sub1",
        text=["Test Text"],
    )

    with pytest.raises(AttributeError):
        enc.NextPage()()


def test_next_page_get_sensitive():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    EncEntry(
        parent=e,
        name="Sub1",
        text=["Test Text"],
    )

    EncEntry(
        parent=e,
        name="Sub2",
        text=["Test Text"],
    )

    enc.SetEntry(e)()

    assert e == enc.active

    enc.NextPage()()
    result = enc.NextPage().get_sensitive()

    assert result


def test_next_page_get_sensitive_no_active():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    EncEntry(
        parent=e,
        name="Sub1",
        text=["Test Text"],
    )

    result = enc.NextPage().get_sensitive()
    assert not result
