from encyclopaedia.book import Book


def test_book_title():
    book = Book(title="Greek Gods", subject="Mythology")

    assert book.title == "Greek Gods"


def test_book_title_locked():
    book = Book(title="Greek Gods", subject="Mythology", locked=True)

    assert book.title == "???"


def test_book_name():
    book = Book(title="Greek Gods", subject="Mythology")

    assert book.title == book.name
