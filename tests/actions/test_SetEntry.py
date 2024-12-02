from encyclopaedia import EncEntry, Encyclopaedia, constants_ren
from encyclopaedia.book import Book


def test_set_entry(add_dummy_entries):
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    entries = add_dummy_entries(enc, 5)

    add_dummy_entries(enc, 5, locked=True)

    e = entries[-1]

    # Use the last unlocked Entry created for the test.
    enc.SetEntry(e)()

    assert e == enc.active
    assert 4 == enc.current_position


def test_set_entry_sorting_mode_unread(add_dummy_entries):
    """
    When the sorting mode is by unread entries,
    Then the Encyclopaedia should resort when an entry is set
    And the newly read entry is in the correct position
    """

    enc = Encyclopaedia(sorting_mode=constants_ren.SortMode.UNREAD)

    entries = add_dummy_entries(enc, 5)

    e = entries[1]

    assert e == enc.current_entries[1]

    enc.SetEntry(e)()

    assert e == enc.active

    # entry should be moved from 2nd position to the last
    assert e == enc.current_entries[-1]


def test_set_entry_book_viewed():
    enc = Encyclopaedia()

    book = Book(parent=enc, title="Greek Gods", subject="Mythology")
    EncEntry(parent=book, number=0, name="Zeus")
    EncEntry(parent=book, number=1, name="Hades")

    enc.SetEntry(book)()

    assert book.viewed is False
    assert book.active.viewed is True


def test_set_entry_get_sensitive_entry_unlocked():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Entry 1",
        text=["Test Text"],
    )

    action = enc.SetEntry(e)

    result = action.get_sensitive()

    assert result is True


def test_set_entry_get_sensitive_entry_locked():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Entry 1",
        text=["Test Text"],
        locked=True,
    )

    action = enc.SetEntry(e)

    result = action.get_sensitive()

    assert result is False


def test_set_entry_get_selected():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Entry 1",
        text=["Test Text"],
    )

    action = enc.SetEntry(e)

    action()

    result = action.get_selected()

    assert result is True
