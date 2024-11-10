import pytest

from encyclopaedia import EncEntry
from encyclopaedia.book import Book


def test_book_percentage_unlocked():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(number=0, name="Zeus", text="Dummy Text")
    book.add_entry(zeus)

    hades = EncEntry(number=1, name="Hades", locked=True)
    book.add_entry(hades)

    result = book.percentage_unlocked
    assert result == 0.5


def test_percentage_unlocked_empty():
    """When a Book is empty
    Then accessing Book().percentage_unlocked raises a ZeroDivisionError
    """
    book = Book(title="Greek Gods", subject="Mythology")

    with pytest.raises(ZeroDivisionError):
        book.percentage_unlocked
