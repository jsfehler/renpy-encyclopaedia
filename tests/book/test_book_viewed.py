from encyclopaedia.book import Book
from encyclopaedia import EncEntry


def test_book_viewed_none_viewed():
    """When all EncEntry in a Book has not been viewed
    Then the viewed status of the Book is False
    """
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")

    assert book.viewed is False


def test_book_viewed_some_viewed():
    """When any EncEntry in a Book has not been viewed
    Then the viewed status of the Book is False
    """
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")

    zeus.viewed = True

    assert book.viewed is False


def test_book_viewed_all_viewed():
    """When all EncEntry in a Book have been viewed
    Then the viewed status of the Book is True
    """
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    hades = EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")

    zeus.viewed = True

    assert book.viewed is False

    hades.viewed = True

    assert book.viewed is True
