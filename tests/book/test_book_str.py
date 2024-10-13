from encyclopaedia.book import Book


def test_book_str():
    book = Book(number=100, title="Greek Gods", subject="Mythology")

    assert str(book) == "Greek Gods"


def test_book_repr():
    book = Book(number=100, title="Greek Gods", subject="Mythology")

    assert repr(book) == "Book(number=100, title=Greek Gods, subject=Mythology)"
