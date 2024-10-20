from encyclopaedia.book import Book
from encyclopaedia import EncEntry

import pytest


def test_book_set_active_page():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    hades = EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")

    book.set_active_page(1)
    assert book.active == hades


def test_book_set_active_page_invalid_under_zero():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")

    with pytest.raises(ValueError):
        book.set_active_page(-100)

    assert book.active == zeus


def test_book_set_active_page_invalid_over_max():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")

    with pytest.raises(ValueError):
        book.set_active_page(100)

    assert book.active == zeus


def test_book_current_page_alias():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    hades = EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")

    book.set_active_page(1)
    assert book.current_page == book.active
