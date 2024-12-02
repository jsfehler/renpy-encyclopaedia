from encyclopaedia import EncEntry, Encyclopaedia


def test_encentry_lock():
    """
    When an EncEntry is unlocked
    And it's locked
    Then the locked status should update
    """
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    e.locked = True

    assert e.locked is True


def test_encentry_unlock():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=True,

    )

    assert e in enc.all_entries
    assert e not in enc.unlocked_entries

    # Unlock the first entry
    e.locked = False
    assert e.locked is False

    assert e in enc.all_entries
    assert e in enc.unlocked_entries
