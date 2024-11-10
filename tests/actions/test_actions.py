from encyclopaedia import EncEntry, Encyclopaedia, constants_ren


def test_viewed_callback_set_entry():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    global i
    i = 0

    @e.on("viewed")
    def cb(entry):
        global i
        i += 1

    assert 0 == i

    enc.SetEntry(e)()

    assert 1 == i


def test_viewed_callback_change_entry():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    e2 = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    global i
    i = 0

    @e2.on("viewed")
    def cb(entry):
        global i
        i += 1

    assert 0 == i

    enc.SetEntry(e)()
    assert 0 == i

    enc.NextEntry()()

    assert 1 == i


def test_viewed_callback_multiple():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    global i
    i = 0

    global j
    j = 50

    @e.on("viewed")
    def cb(entry):
        global i
        i += 1

    @e.on("viewed")
    def cb2(entry):
        global j
        j += 10

    assert 0 == i
    assert 50 == j

    enc.SetEntry(e)()

    assert 1 == i
    assert 60 == j


def test_reset_sub_page():
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

    eee = EncEntry(
        parent=e,
        name="Sub2",
        text=["Test Text"],
    )

    enc.SetEntry(e)()

    assert e == enc.active
    assert enc.active._unlocked_page_index == 0

    enc.NextPage()()
    enc.NextPage()()

    assert enc.active._unlocked_page_index == 2
    assert e.current_page == eee

    enc.ResetSubPage()()

    assert enc.active._unlocked_page_index == 0
    assert e.current_page == e


def test_toggle_show_locked_buttons():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for _ in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False,
        )

    enc.ToggleShowLockedButtons()()

    assert True is enc.show_locked_buttons


def test_toggle_show_locked_buttons_reverse_sorting():
    """Ensure reverse sorting isn't broken when toggling show_locked_buttons."""

    enc = Encyclopaedia(sorting_mode=constants_ren.SortMode.REVERSE_ALPHABETICAL)

    entry_names = ["Apple", "Carrot", "Deer", "Eel", "Fajita"]

    for x in range(5):
        EncEntry(
            parent=enc,
            name=entry_names[x],
            text=["Test Text"],
            locked=False,
        )

    locked_entry = EncEntry(
        parent=enc,
        name="Banana",
        text=["Test Text"],
        locked=True,
    )

    # Locked entry should be the first entry, due to reverse sorting
    assert str(enc.all_entries[0]) == str(locked_entry)

    # Locked entry should not be visible on screen
    assert locked_entry not in enc.current_entries

    # Start showing locked buttons
    enc.ToggleShowLockedButtons()()

    assert str(enc.current_entries[0]) == str(locked_entry)


def test_toggle_show_locked_entry():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for _ in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False,
        )

    enc.ToggleShowLockedEntry()()

    assert True is enc.show_locked_entry


def test_sort_encyclopaeda():
    """Test Actions through their implementation in Encyclopaedia."""

    enc = Encyclopaedia()

    for _ in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False,
        )

    enc.Sort(sorting_mode=constants_ren.SortMode.SUBJECT)()

    assert constants_ren.SortMode.SUBJECT == enc.sorting_mode
