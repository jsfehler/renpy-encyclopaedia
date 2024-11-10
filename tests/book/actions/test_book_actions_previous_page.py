from encyclopaedia import EncEntry
from encyclopaedia.book import Book


def test_book_actions_previous_page():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    hades = EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.next_page()
    book.next_page()

    book.actions.PreviousPage()()

    assert book.active == hades


def test_book_actions_previous_page_get_sensitive():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.actions.NextPage()()
    book.actions.NextPage()()
    result = book.actions.PreviousPage().get_sensitive()

    assert result


def test_book_actions_previous_page_get_sensitive_stop_at_zero():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    # Force an active page
    book.set_active_page(0)

    book.actions.NextPage()()

    result = book.actions.PreviousPage().get_sensitive()
    assert result

    book.actions.PreviousPage()()
    result = book.actions.PreviousPage().get_sensitive()
    assert not result
