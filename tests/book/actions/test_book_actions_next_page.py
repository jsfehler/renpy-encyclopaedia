from encyclopaedia import EncEntry
from encyclopaedia.book import Book


def test_book_actions_next_page():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    hades = EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.actions.NextPage()()

    assert book.active == hades


def test_book_actions_next_page_get_sensitive():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.actions.NextPage()()
    result = book.actions.NextPage().get_sensitive()

    assert result


def test_book_actions_next_page_get_sensitive_stop_at_max():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.actions.NextPage()()

    result = book.actions.NextPage().get_sensitive()
    assert result

    book.actions.NextPage()()
    result = book.actions.NextPage().get_sensitive()
    assert not result
