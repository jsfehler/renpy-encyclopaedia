from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry


def test_reset_sub_page():
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

    eee = EncEntry(
        parent=e,
        name="Sub2",
        text=["Test Text"],
    )

    enc.SetEntry(e)()

    assert e == enc.active
    assert enc.sub_current_position == 1

    enc.NextPage()()
    enc.NextPage()()

    assert enc.sub_current_position == 3
    assert e.current_page == eee

    enc.ResetSubPage()()

    assert enc.sub_current_position == 1
    assert e.current_page == e


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

    eee = EncEntry(
        parent=e,
        name="Sub2",
        text=["Test Text"],
    )

    enc.SetEntry(e)()

    assert e == enc.active
    assert enc.sub_current_position == 1

    enc.NextPage()()

    assert enc.sub_current_position == 2
    assert e.current_page == ee


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


def test_next_entry():
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

    assert enc.current_entries[1] == enc.active
    assert enc.current_entries[1].viewed
    assert 1 == enc.current_position


def test_set_entry():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for x in range(5):
        e = EncEntry(
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

    # Use the last unlocked Entry created for the test.
    enc.SetEntry(e)()

    assert e == enc.active
    assert 4 == enc.current_position


def test_filter_by_subject():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    expected_entries = []

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            subject="Robots"
        )

        expected_entries.append(e)

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            subject="Humans"
        )

    enc.FilterBySubject("Robots")()

    assert "Robots" == enc.filtering
    assert expected_entries == enc.filtered_entries


def test_toggle_show_locked_buttons():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )

    enc.ToggleShowLockedButtons()()

    assert True is enc.show_locked_buttons


def test_toggle_show_locked_entry():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )

    enc.ToggleShowLockedEntry()()

    assert True is enc.show_locked_entry


def test_sort_encyclopaeda():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )

    enc.Sort(sorting_mode=Encyclopaedia.SORT_SUBJECT)()

    assert Encyclopaedia.SORT_SUBJECT == enc.sorting_mode
