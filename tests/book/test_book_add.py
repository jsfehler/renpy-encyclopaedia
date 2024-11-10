import pytest

from encyclopaedia import EncEntry, Encyclopaedia
from encyclopaedia.book import Book
from encyclopaedia.exceptions_ren import AddEntryError


def test_book_add_entry():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(number=0, name="Zeus", text="Dummy Text")

    result = book.add_entry(zeus)
    assert result is True


def test_book_add_entry_dupe():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(number=0, name="Zeus", text="Dummy Text")

    book.add_entry(zeus)

    with pytest.raises(AddEntryError):
        book.add_entry(zeus)


def test_book_add_entry_no_number():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(name="Zeus", text="Dummy Text")

    with pytest.raises(AddEntryError):
        book.add_entry(zeus)


def test_book_add_entry_parent_already_set():
    enc = Encyclopaedia()

    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(parent=enc, number=0, name="Zeus", text="Dummy Text")

    with pytest.raises(AddEntryError):
        book.add_entry(zeus)


def test_book_add_entry_number_taken():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(number=0, name="Zeus", text="Dummy Text")
    book.add_entry(zeus)

    hades = EncEntry(number=0, name="Hades", text="Dummy Text")

    with pytest.raises(AddEntryError):
        book.add_entry(hades)


def test_book_add_entry_subject_already_set():
    enc = Encyclopaedia()

    book = Book(parent=enc, title="Greek Gods", subject="Mythology")

    zeus = EncEntry(number=0, name="Zeus", text="Dummy Text", subject="Mythology")

    with pytest.raises(AddEntryError):
        book.add_entry(zeus)


def test_book_add_entry_recalculate_word_count():
    book = Book(title="Greek Gods", subject="Mythology")

    assert book.word_count == 0

    zeus = EncEntry(number=0, name="Zeus", text="Dummy Text")
    book.add_entry(zeus)

    assert book.word_count == 2
