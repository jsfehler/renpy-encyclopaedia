from encyclopaedia import EncEntry, Encyclopaedia


def test_next_entry():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name=f"Test Name {x + 1}",
            text=["Test Text"],
            locked=False,
        )

    assert 0 == enc.current_position

    enc.NextEntry()()

    assert enc.current_entries[1] == enc.active
    assert enc.current_entries[1].viewed
    assert 1 == enc.current_position


def test_next_entry_get_sensitive():
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
    result = enc.NextEntry().get_sensitive()

    assert result


def test_next_entry_get_sensitive_no_active():
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Entry 1",
        text=["Test Text"],
    )

    assert enc.active is None

    result = enc.NextEntry().get_sensitive()
    assert result is False
