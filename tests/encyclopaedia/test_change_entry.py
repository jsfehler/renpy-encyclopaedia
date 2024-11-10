from encyclopaedia import EncEntry, Encyclopaedia, constants_ren
from encyclopaedia.book import Book


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

def test_change_entry_book():
    """
    When I change entry to a Book
    Then only the first page is marked as viewed
    """
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    book = Book(parent=enc, title="Greek Gods", subject="Mythology")
    page_0 = EncEntry(
        parent=book,
        number=0,
        name="Zeus",
        text="",
    )
    page_1 = EncEntry(
        parent=book,
        number=1,
        name="Hades",
        text="",
    )

    assert page_0.viewed is False

    enc._change_entry(constants_ren.Direction.FORWARD)

    assert page_0.viewed is True
    assert page_1.viewed is False
    assert book.viewed is False
