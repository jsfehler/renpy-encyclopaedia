import pytest

from encyclopaedia import EncEntry, Encyclopaedia, constants_ren


@pytest.fixture()
def sortable_enc():
    """Create an encyclopaedia for filtering tests."""
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Apple",
        text=[""],
        subject="Fruit",
    )

    EncEntry(
        parent=enc,
        name="Banana",
        text=[""],
        subject="Fruit",
    )

    EncEntry(
        parent=enc,
        name="Grape",
        text=[""],
        subject="Fruit",
    )

    return enc


def test_sort_encyclopaedia_reverse_alphabetical(sortable_enc):
    """Test Actions through their implementation in Encyclopaedia."""
    action = sortable_enc.Sort(constants_ren.SortMode.REVERSE_ALPHABETICAL)

    assert sortable_enc.current_entries[0].name == "Apple"

    action()

    assert sortable_enc.current_entries[0].name == "Grape"


def test_sort_encyclopaedia_get_selected(sortable_enc):
    """Test Actions through their implementation in Encyclopaedia."""
    action = sortable_enc.Sort(constants_ren.SortMode.SUBJECT)
    action()

    result = action.get_selected()

    assert result is True


def test_sort_encyclopaedia_get_selected_no_filter(sortable_enc):
    """Test Actions through their implementation in Encyclopaedia."""
    action = sortable_enc.Sort(constants_ren.SortMode.SUBJECT)

    result = action.get_selected()

    assert result is False


def test_sort_encyclopaedia_reverse_alphabetical_reverse(sortable_enc):
    """Test Actions through their implementation in Encyclopaedia."""
    action = sortable_enc.Sort(
        constants_ren.SortMode.REVERSE_ALPHABETICAL,
        reverse=True,
    )

    assert sortable_enc.current_entries[0].name == "Apple"

    action()

    assert sortable_enc.current_entries[0].name == "Apple"
