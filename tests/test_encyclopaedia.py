import pytest

from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry
from encyclopaedia import constants_ren


def test_setting_entry_number(add_dummy_entries):
    """
    When some entries have a pre-determined number,
    And some do not,
    Then the ones that do not should select the first available number.
    """

    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        number=4,
        name="Apple",
        text=["Test Text"],
    )

    entries = add_dummy_entries(enc, 5)

    assert 6 == entries[-1].number


def test_filtering():
    enc = Encyclopaedia()

    apple = EncEntry(
        parent=enc,
        name="Apple",
        text=["Test Text"],
        subject="Fruits"
    )

    banana = EncEntry(
        parent=enc,
        name="Banana",
        text=["Test Text"],
        subject="Fruits"
    )

    cantaloupe = EncEntry(
        parent=enc,
        name="Cantaloupe",
        text=["Test Text"],
        subject="Fruits"
    )

    EncEntry(
        parent=enc,
        name="Cucumber",
        text=["Test Text"],
        subject="Vegetables"
    )

    enc.FilterBySubject("Fruits")()

    assert "Fruits" == enc.filtering
    assert [apple, banana, cantaloupe] == enc.current_entries


def test_clear_filtering():
    enc = Encyclopaedia()

    apple = EncEntry(
        parent=enc,
        name="Apple",
        text=["Test Text"],
        subject="Fruits"
    )

    banana = EncEntry(
        parent=enc,
        name="Banana",
        text=["Test Text"],
        subject="Fruits"
    )

    cantaloupe = EncEntry(
        parent=enc,
        name="Cantaloupe",
        text=["Test Text"],
        subject="Fruits"
    )

    cucumber = EncEntry(
        parent=enc,
        name="Cucumber",
        text=["Test Text"],
        subject="Vegetables"
    )

    enc.FilterBySubject("Fruits")()

    assert "Fruits" == enc.filtering
    assert [apple, banana, cantaloupe] == enc.current_entries

    enc.ClearFilter()()

    assert False is enc.filtering
    assert [apple, banana, cantaloupe, cucumber] == enc.current_entries


def test_reverse_alphabetical_sorting():
    enc = Encyclopaedia(sorting_mode=constants_ren.SortMode.REVERSE_ALPHABETICAL)

    apple = EncEntry(
        parent=enc,
        name="Apple",
        text=["Test Text"],
    )

    banana = EncEntry(
        parent=enc,
        name="Banana",
        text=["Test Text"],
    )

    cantaloupe = EncEntry(
        parent=enc,
        name="Cantaloupe",
        text=["Test Text"],
    )

    assert [cantaloupe, banana, apple] == enc.all_entries


def test_unlock_callback():
    enc = Encyclopaedia()

    global baz
    baz = 0

    @enc.on("entry_unlocked")
    def foobar(enc):
        global baz
        baz += 1

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=True,
    )

    # Unlock the first entry
    e.locked = False
    assert e.locked is False

    assert 1 == baz


def test_duplicate_entry_numbers():
    """When trying to assign a number to an EncEntry that's already taken,
    an Exception should be thrown.
    """
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False
    )

    EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False
    )

    with pytest.raises(ValueError) as e:
        EncEntry(
            parent=enc,
            number=1,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )

    message = '1 is already taken.'
    assert message == str(e.value)


def test_set_entry_show_locked_buttons(add_dummy_entries):
    """Given an Encyclopaedia with 10 unlocked entries and 5 locked entries,
    And show_locked_buttons is true,
    When I set the 10th unlocked entry to be the active entry,
    Then the entry should be marked as viewed,
    And the entry should be the active entry,
    And the Encyclopaedia's current_position should be 9
    """
    enc = Encyclopaedia(show_locked_buttons=True, show_locked_entry=False)

    add_dummy_entries(enc, 5)

    add_dummy_entries(enc, 5, locked=True)

    entries = add_dummy_entries(enc, 5)

    # Use the last unlocked Entry created for the test.
    e = entries[-1]
    enc.SetEntry(e)()

    assert e == enc.active
    assert e.viewed
    assert 9 == enc.current_position


def test_set_entry_show_locked_entry(add_dummy_entries):
    """Given an Encyclopaedia with 10 unlocked entries and 5 locked entries,
    And show_locked_entry is true,
    When I set the 10th unlocked entry to be the active entry,
    Then the entry should be marked as viewed,
    And the entry should be the active entry,
    And the Encyclopaedia's current_position should be 14
    """
    enc = Encyclopaedia(show_locked_buttons=False, show_locked_entry=True)

    add_dummy_entries(enc, 5)

    add_dummy_entries(enc, 5, locked=True)

    entries = add_dummy_entries(enc, 5)

    # Use the last unlocked Entry created for the test.
    e = entries[-1]
    enc.SetEntry(e)()

    assert e == enc.active
    assert e.viewed
    assert 14 == enc.current_position


def test_current_entries_show_unlocked(add_dummy_entries):
    """With filtering off and show_locked_buttons set to False,
    Encyclopaedia.current_entries property should return
    Encyclopaedia.unlocked_entries.
    """

    enc = Encyclopaedia()

    expected_list = add_dummy_entries(enc, 5)

    add_dummy_entries(enc, 5, locked=True)

    assert expected_list == enc.current_entries


def test_current_entries_show_all(add_dummy_entries):
    """With filtering off and show_locked_buttons set to True,
    Encyclopaedia.current_entries property should return
    Encyclopaedia.all_entries.
    """

    enc = Encyclopaedia(show_locked_buttons=True)

    expected_list = add_dummy_entries(enc, 5)

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=True
        )
        expected_list.append(e)

    assert expected_list == enc.current_entries


def test_current_entry(add_dummy_entries):
    enc = Encyclopaedia()

    add_dummy_entries(enc, 4, locked=True)

    EncEntry(
        parent=enc,
        name="Dummy Name 5",
        text=["Dummy Text"],
        locked=False,
    )

    assert str(enc.current_entry) == "05: Dummy Name 5"


def test_current_entry_show_locked_entry(add_dummy_entries):
    enc = Encyclopaedia(show_locked_entry=True)

    add_dummy_entries(enc, 4, locked=True)

    EncEntry(
        parent=enc,
        name="Dummy Name 5",
        text=["Dummy Text"],
        locked=False,
    )

    assert str(enc.current_entry) == "01: ???"


def test_percentage_unlocked(add_dummy_entries):
    """Base unit test for the
    Encyclopaedia.percentage_unlocked property.
    """

    enc = Encyclopaedia()

    add_dummy_entries(enc, 5)

    add_dummy_entries(enc, 5, locked=True)

    assert 50.00 == enc.percentage_unlocked


def test_percentage_unlocked_empty():
    """When an encyclopaedia is empty,
    Then accessing percentage_unlocked raises an Exception.
    And provide a readable error message.
    """
    enc = Encyclopaedia()

    with pytest.raises(ZeroDivisionError) as e:
        enc.percentage_unlocked

    message = 'Cannot calculate percentage unlocked of empty Encyclopaedia'
    assert message == str(e.value)


def test_word_count(add_dummy_entries):
    """When checking the word count of an Encyclopaedia,
    Then the number returned is correct.
    """
    enc = Encyclopaedia()

    add_dummy_entries(enc, 5)

    assert 10 == enc.word_count


def test_word_count_locked(add_dummy_entries):
    """When checking the word count of an Encyclopaedia,
    And entries are locked,
    Then the number returned is correct.
    """
    enc = Encyclopaedia()

    add_dummy_entries(enc, 5, locked=True)

    assert 10 == enc.word_count


def test_add_entry_already_in_page():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    ee = EncEntry(
        parent=e,
        name="Test Page",
        text=["Test Text"],
    )

    with pytest.raises(ValueError):
        enc.add_entry(ee)


def test_change_entry_boundary_forward():
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    EncEntry(
        parent=enc,
        name="Test Name 2",
        text=["Test Text"],
    )

    result = enc._change_entry(constants_ren.Direction.FORWARD)
    assert result

    result = enc._change_entry(constants_ren.Direction.FORWARD)
    assert not result


def test_change_entry_boundary_back():
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    result = enc._change_entry(constants_ren.Direction.BACKWARD)
    assert not result


def test_repr():
    enc = Encyclopaedia(name="Dummy Enc Name")

    EncEntry(parent=enc, name="Dummy EncEntry", text="Dummy Text")

    assert repr(enc) == "Encyclopaedia(name=Dummy Enc Name, length=1)"


def test_str():
    enc = Encyclopaedia(name="Dummy Enc Name")

    EncEntry(parent=enc, name="Dummy EncEntry", text="Dummy Text")

    assert str(enc) == "Encyclopaedia: Dummy Enc Name"


def test_number_of_visible_entries(add_dummy_entries):
    enc = Encyclopaedia(name="Dummy Enc Name")

    add_dummy_entries(enc, 5)

    add_dummy_entries(enc, 7, locked=True)

    assert enc.number_of_visible_entries == 5


def test_number_of_visible_entries_show_locked_entry(add_dummy_entries):
    enc = Encyclopaedia(name="Dummy Enc Name", show_locked_entry=True)

    add_dummy_entries(enc, 5)

    add_dummy_entries(enc, 7, locked=True)

    assert enc.number_of_visible_entries == 12
