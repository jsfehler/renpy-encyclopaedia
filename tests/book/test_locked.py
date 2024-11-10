from renpy.game import persistent

from encyclopaedia import EncEntry, Encyclopaedia
from encyclopaedia.book import Book


def test_book_unlock():
    book = Book(title="Greek Gods", subject="Mythology", locked=True)

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    book.locked = False

    assert book.locked is False


def test_book_unlock_page():
    book = Book(title="Greek Gods", subject="Mythology")

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    poseidon = EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text", locked=True)

    assert poseidon not in book.unlocked_pages

    poseidon.locked = False

    assert poseidon in book.unlocked_pages


def test_book_unlock_persistent_first_get():
    book = Book(title="Greek Gods", subject="Mythology", locked=False, locked_persistent=True)

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    assert book.locked is False

    assert persistent.greek_gods_locked is False


def test_book_unlock_persistent_get():
    book = Book(title="Greek Gods", subject="Mythology", locked=True, locked_persistent=True)

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    assert book.locked == persistent.greek_gods_locked


def test_book_unlock_persistent_set():
    book = Book(title="Greek Gods", subject="Mythology", locked=True, locked_persistent=True)

    EncEntry(parent=book, number=0, name="Zeus", text="Dummy Text")
    EncEntry(parent=book, number=1, name="Hades", text="Dummy Text")
    EncEntry(parent=book, number=2, name="Poseidon", text="Dummy Text")

    book.locked = False

    assert book.locked is False
    assert persistent.greek_gods_locked is False


def test_book_unlock_parent_event():
    enc = Encyclopaedia()

    def event_func(source):
        assert source == enc

    enc.on('entry_unlocked')(event_func)

    book = Book(parent=enc, title="Greek Gods", subject="Mythology", locked=True)

    book.locked = False
