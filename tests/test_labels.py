from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry


def test_sorting_mode_label():
    enc = Encyclopaedia()

    for x in range(5):
        EncEntry(
            parent=enc,
            name="Test Name",
            text=["Test Text"],
            subject="Test Subject",
        )

    assert "Number" == enc.labels.sorting_mode

    enc.Sort(Encyclopaedia.SORT_ALPHABETICAL)()
    assert "A to Z" == enc.labels.sorting_mode

    enc.Sort(Encyclopaedia.SORT_REVERSE_ALPHABETICAL)()
    assert "Z to A" == enc.labels.sorting_mode

    enc.Sort(Encyclopaedia.SORT_SUBJECT)()
    assert "Subject" == enc.labels.sorting_mode

    enc.Sort(Encyclopaedia.SORT_UNREAD)()
    assert "Unread" == enc.labels.sorting_mode


def test_percentage_unlocked_label():
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

    assert "50%" == enc.labels.percentage_unlocked
