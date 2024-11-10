import pytest

from encyclopaedia import EncEntry, Encyclopaedia


@pytest.fixture()
def filterable_enc():
    """Create an encyclopaedia for filtering tests."""
    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name=f"Robot: {x}",
            text=[""],
            subject="Robots",
        )

    for x in range(5):
        EncEntry(
            parent=enc,
            name=f"Human: {x}",
            text=[""],
            subject="Humans",
        )

    return enc


def test_filter_by_subject(filterable_enc):
    """Test Actions through their implementation in Encyclopaedia."""
    filterable_enc.FilterBySubject("Robots")()

    assert "Robots" == filterable_enc.filtering
    assert len(filterable_enc.filtered_entries) == 5

    for i in filterable_enc.filtered_entries:
        assert "Robot:" in i.name


def test_filter_by_subject_get_selected(filterable_enc):
    """Test Actions through their implementation in Encyclopaedia."""
    action = filterable_enc.FilterBySubject("Robots")
    action()

    result = action.get_selected()

    assert result is True


def test_filter_by_subject_get_selected_no_filter(filterable_enc):
    """Test Actions through their implementation in Encyclopaedia."""
    action = filterable_enc.FilterBySubject("Robots")

    result = action.get_selected()

    assert result is False
