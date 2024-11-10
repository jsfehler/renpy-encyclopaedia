from unittest.mock import patch

import pytest

from encyclopaedia import EncEntry, Encyclopaedia
from encyclopaedia.book import Book
from encyclopaedia.exceptions_ren import InvalidEntryAnchorError
from encyclopaedia.hyperlink_ren import set_encentry_from_text_anchor


@patch("encyclopaedia.hyperlink_ren.store")
def test_set_encentry_from_text_anchor(mock):
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        number=4,
        name="Apple",
        text=["Test Text"],
    )

    # Immitate renpy.store
    mock.enc = enc
    mock.e = e

    set_encentry_from_text_anchor("enc->e")

    assert enc.active == e


@patch("encyclopaedia.hyperlink_ren.store")
def test_set_encentry_from_text_anchor_book(mock):
    enc = Encyclopaedia()

    book = Book(parent=enc, title="Greek Gods", subject="Mythology")

    # Immitate renpy.store
    mock.enc = enc
    mock.book = book

    set_encentry_from_text_anchor("enc->book->0")

    assert enc.active == book


@patch("encyclopaedia.hyperlink_ren.store")
def test_set_encentry_from_text_anchor_invalid(mock):
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        number=4,
        name="Apple",
        text=["Test Text"],
    )

    # Immitate renpy.store
    mock.enc = enc
    mock.e = e

    with pytest.raises(InvalidEntryAnchorError):
        set_encentry_from_text_anchor("enc")
