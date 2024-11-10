from encyclopaedia import EncEntry, Encyclopaedia


def test_close_active_entry_active_cleared():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    enc.SetEntry(e)()

    assert enc.active == e

    enc.CloseActiveEntry()()

    assert enc.active is None
