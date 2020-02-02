import pytest

from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry


def test_setting_entry_number():
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

    for x in range(0, 5):
        e = EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
        )

    assert 6 == e.number


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

    cucumber = EncEntry(
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
    enc = Encyclopaedia(sorting_mode=Encyclopaedia.SORT_REVERSE_ALPHABETICAL)

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


def test_set_entry_show_locked_buttons():
    """Given an Encyclopaedia with 10 unlocked entries and 5 locked entries,
    And show_locked_buttons is true,
    When I set the 10th unlocked entry to be the active entry,
    Then the entry should be marked as viewed,
    And the entry should be the active entry,
    And the Encyclopaedia's current_position should be 9
    """
    enc = Encyclopaedia(show_locked_buttons=True, show_locked_entry=False)

    for x in range(0, 5):
        EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
            locked=False
        )

    for x in range(5, 10):
        EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
            locked=True
        )

    for x in range(10, 15):
        e = EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
            locked=False
        )

    # Use the last unlocked Entry created for the test.
    enc.SetEntry(e)()

    assert e == enc.active
    assert e.viewed
    assert 9 == enc.current_position


def test_set_entry_show_locked_entry():
    """Given an Encyclopaedia with 10 unlocked entries and 5 locked entries,
    And show_locked_entry is true,
    When I set the 10th unlocked entry to be the active entry,
    Then the entry should be marked as viewed,
    And the entry should be the active entry,
    And the Encyclopaedia's current_position should be 14
    """
    enc = Encyclopaedia(show_locked_buttons=False, show_locked_entry=True)

    for x in range(0, 5):
        EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
            locked=False
        )

    for x in range(5, 10):
        EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
            locked=True
        )

    for x in range(10, 15):
        e = EncEntry(
            parent=enc,
            name="Test Name {}".format(x + 1),
            text=["Test Text"],
            locked=False
        )

    # Use the last unlocked Entry created for the test.
    enc.SetEntry(e)()

    assert e == enc.active
    assert e.viewed
    assert 14 == enc.current_position


def test_current_entries_show_unlocked():
    """With filtering off and show_locked_buttons set to False,
    Encyclopaedia.current_entries property should return
    Encyclopaedia.unlocked_entries.
    """

    enc = Encyclopaedia()

    expected_list = []

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )
        expected_list.append(e)

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=True
        )

    assert expected_list == enc.current_entries


def test_current_entries_show_all():
    """With filtering off and show_locked_buttons set to True,
    Encyclopaedia.current_entries property should return
    Encyclopaedia.all_entries.
    """

    enc = Encyclopaedia(show_locked_buttons=True)

    expected_list = []

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=False
        )
        expected_list.append(e)

    for x in range(5):
        e = EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            locked=True
        )
        expected_list.append(e)

    assert expected_list == enc.current_entries


def test_percentage_unlocked():
    """Base unit test for the
    Encyclopaedia.percentage_unlocked property.
    """

    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
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
