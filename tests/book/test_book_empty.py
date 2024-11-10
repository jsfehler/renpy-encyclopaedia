import pytest

from encyclopaedia import EncEntry
from encyclopaedia.book import Book
from encyclopaedia.exceptions_ren import GetEntryError


def test_book_empty_get_active():
    book = Book(title="Greek Gods", subject="Mythology")

    with pytest.raises(GetEntryError) as e:
        book.active

    assert str(e.value) == "Book has no pages."


def test_book_empty_get_active_bad_index():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")

    book._unlocked_page_index = 1

    with pytest.raises(GetEntryError) as e:
        book.active

    assert str(e.value) == "Tried to fetch page at index: <1>. Maximum value is: <0>"
