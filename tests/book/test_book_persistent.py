from encyclopaedia.book import Book


def test_book_get_persistent_name():
    book = Book(title="Greek Gods", subject="Mythology")

    result = book._get_persistent_name()
    assert result == "greek_gods_locked"
