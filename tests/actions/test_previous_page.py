import pytest

from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry


def test_previous_page():
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
    assert enc.sub_current_position == 1

    enc.NextPage()()
    enc.PreviousPage()()

    assert e == e.current_page
    assert enc.sub_current_position == 1


def test_previous_page_no_active():
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
        enc.PreviousPage()()


def test_previous_page_get_sensitive():
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
    enc.NextPage()()
    result = enc.PreviousPage().get_sensitive()

    assert result


def test_previous_page_get_sensitive_no_active():
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

    result = enc.PreviousPage().get_sensitive()
    assert not result
