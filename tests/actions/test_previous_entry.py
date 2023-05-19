from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry


def test_previous_entry():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for x in range(0, 5):
        EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
            locked=False
        )

    assert 0 == enc.current_position

    enc.NextEntry()()

    enc.PreviousEntry()()

    assert enc.current_entries[0] == enc.active
    assert enc.current_entries[0].viewed
    assert 0 == enc.current_position


def test_previous_entry_get_sensitive():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Entry 1",
        text=["Test Text"],
    )

    EncEntry(
        parent=enc,
        name="Entry 2",
        text=["Test Text"],
    )

    EncEntry(
        parent=enc,
        name="Entry 3",
        text=["Test Text"],
    )

    enc.SetEntry(e)()

    assert e == enc.active

    enc.NextEntry()()
    enc.NextEntry()()
    result = enc.PreviousEntry().get_sensitive()

    assert result


def test_previous_entry_get_sensitive_no_active():
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Entry 1",
        text=["Test Text"],
    )

    EncEntry(
        parent=enc,
        name="Entry 2",
        text=["Test Text"],
    )

    result = enc.PreviousEntry().get_sensitive()
    assert not result
