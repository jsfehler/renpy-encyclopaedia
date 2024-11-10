from encyclopaedia import EncEntry
from encyclopaedia.book import Book


def test_book_next_page():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    hades = EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    result = book.next_page()
    assert result is True

    assert book.active == hades


def test_book_next_page_hit_bounds():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    poseidon = EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.next_page()
    book.next_page()
    result = book.next_page()
    assert result is False

    assert book.active == poseidon


def test_book_previous_page():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    hades = EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.next_page()
    book.next_page()
    result = book.previous_page()
    assert result is True

    assert book.active == hades


def test_book_previous_page_hit_bounds():
    book = Book(title="Greek Gods", subject="Mythology")

    zeus = EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    result = book.previous_page()
    assert result is False

    assert book.active == zeus
