import pytest

from encyclopaedia import EncEntry, Encyclopaedia


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
    assert enc.active._unlocked_page_index == 0

    enc.NextPage()()
    enc.PreviousPage()()

    assert e == e.current_page
    assert enc.active._unlocked_page_index == 0


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


def test_previous_page_get_sensitive_stop_at_zero():
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

    result = enc.PreviousPage().get_sensitive()
    assert result

    enc.PreviousPage()()
    result = enc.PreviousPage().get_sensitive()
    assert not result


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
